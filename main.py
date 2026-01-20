#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Main entry point for automated content publishing."""

import os
import sys
import io

# Set UTF-8 encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from dotenv import load_dotenv

from src.generators.topic_generator import TopicGenerator
from src.generators.content_generator import ContentGenerator
from src.generators.image_generator import ImageGenerator
from src.validators.seo_validator import SEOValidator
from src.publishers.wordpress import WordPressPublisher
from src.utils.database import TopicDatabase
from src.utils.logger import StructuredLogger
from src.utils.schedule import get_next_publish_time, should_schedule


def main():
    """Execute content publishing pipeline."""
    # Load environment variables
    load_dotenv()

    # Validate environment variables
    required_vars = [
        "ANTHROPIC_API_KEY",
        "WORDPRESS_URL",
        "WORDPRESS_USERNAME",
        "WORDPRESS_APP_PASSWORD"
    ]

    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}")
        print("Please set them in .env file")
        return 1

    # Initialize components
    logger = StructuredLogger()
    db = TopicDatabase()

    print("\n" + "="*60)
    print("Automated Content Publishing System")
    print("Tarot x Love x MBTI -> WordPress")
    print("="*60 + "\n")

    try:
        # Step 1: Generate unique topic
        print("Step 1/6: Generating unique topic...")
        topic_gen = TopicGenerator(db, logger)
        topic = topic_gen.generate_unique_topic()

        print(f"  MBTI: {topic['mbti']}")
        print(f"  Love: {topic['love_situation'][:30]}...")
        card_type = topic.get('card_type', 'tarot').upper()
        print(f"  {card_type}: {topic['tarot_card']} ({topic['tarot_korean']})")

        # Step 2: Generate content with Claude API
        print("\nStep 2/6: Generating content with Claude API...")
        content_gen = ContentGenerator(logger=logger)
        result = content_gen.generate_content(topic)

        print(f"  Title: {result['title'][:50]}...")
        print(f"  Content length: {len(result['content'])} characters")

        # Display SEO metadata
        if 'metadata' in result and result['metadata']:
            meta = result['metadata']
            if meta.get('meta_description'):
                print(f"  Meta description: {meta['meta_description'][:60]}...")
            if meta.get('image_alt'):
                print(f"  Image alt: {meta['image_alt'][:60]}...")

        # Step 3: Generate AI image
        print("\nStep 3/6: Generating AI image with DALL-E 3...")
        image_gen = ImageGenerator(logger=logger)
        image_result = image_gen.generate_image(topic)

        print(f"  Image generated successfully")

        # Step 4: Validate SEO and safety
        print("\nStep 4/6: Validating SEO and safety...")
        validator = SEOValidator(logger)
        is_valid, issues = validator.validate(result['title'], result['content'])

        if not is_valid:
            print(f"  [WARN] Validation issues: {', '.join(issues)}")
            print("  Auto-sanitizing content...")
            result['content'] = validator.sanitize_content(result['content'])
            is_valid, issues = validator.validate(result['title'], result['content'])

        if is_valid:
            print("  Validation passed")
        else:
            print("  [WARN] Publishing as draft due to validation issues")

        # Step 5: Convert to HTML with JSON-LD schema
        print("\nStep 5/6: Converting to HTML...")
        wp = WordPressPublisher(logger=logger)
        metadata = result.get('metadata')
        html_content = wp.format_content_html(
            result['content'],
            title=result['title'],
            metadata=metadata
        )

        print(f"  HTML generated ({len(html_content)} characters)")

        # Prepare categories and tags
        categories = []
        tags = []

        try:
            cat_id = wp.get_or_create_category(f"MBTI {topic['mbti']}")
            if cat_id:
                categories.append(cat_id)

            tag_mbti = wp.get_or_create_tag(topic['mbti'])
            tag_tarot = wp.get_or_create_tag(topic['tarot_card'])

            if tag_mbti:
                tags.append(tag_mbti)
            if tag_tarot:
                tags.append(tag_tarot)

            print(f"  Categories: {len(categories)}, Tags: {len(tags)}")

        except Exception as e:
            print(f"  [WARN] Category/tag creation failed: {e}")

        # Step 6: Publish to WordPress with image
        print("\nStep 6/6: Publishing to WordPress REST API...")

        # Determine if should schedule or publish immediately
        if should_schedule():
            status = "future"
            scheduled_date = get_next_publish_time()
            print(f"  Scheduling for: {scheduled_date}")
        else:
            status = os.getenv("WORDPRESS_STATUS", "publish")
            scheduled_date = None
            print(f"  Publishing immediately")

        publish_result = wp.publish_post(
            title=result['title'],
            content=html_content,
            status=status,
            categories=categories,
            tags=tags,
            scheduled_date=scheduled_date,
            metadata=metadata
        )

        print(f"  Post published!")
        print(f"  Post ID: {publish_result['post_id']}")
        print(f"  URL: {publish_result['url']}")
        print(f"  Status: {publish_result['status']}")

        # Upload and set featured image
        print("  Uploading featured image...")
        filename = f"{topic['mbti']}_{topic['tarot_card'].replace(' ', '_')}.jpg"

        # Use metadata alt text if available, otherwise use default
        if 'metadata' in result and result['metadata'].get('image_alt'):
            alt_text = result['metadata']['image_alt']
        else:
            alt_text = f"{topic['mbti']} {topic['love_situation']} {topic['tarot_korean']}"

        media_id = wp.upload_image(
            image_data=image_result['data'],
            filename=filename,
            alt_text=alt_text
        )

        if media_id:
            wp.set_featured_image(publish_result['post_id'], media_id)
            print(f"  Featured image set (Media ID: {media_id})")
        else:
            print("  [WARN] Failed to upload image")

        # Save to database
        db.save_published_topic(
            mbti=topic['mbti'],
            love_situation=topic['love_situation'],
            tarot_card=topic['tarot_card'],
            title=result['title'],
            post_id=publish_result['post_id'],
            post_url=publish_result['url'],
            status=publish_result['status']
        )

        print("\n" + "="*60)
        print("Pipeline completed successfully!")
        print("="*60 + "\n")

        return 0

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        logger.error(f"Pipeline failed: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
