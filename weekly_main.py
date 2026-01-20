#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Weekly fortune publishing script - runs on Mondays."""

import os
import sys
import io
from datetime import datetime

# Set UTF-8 encoding for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from dotenv import load_dotenv

from src.generators.weekly_fortune_generator import WeeklyFortuneGenerator
from src.publishers.wordpress import WordPressPublisher
from src.utils.database import TopicDatabase
from src.utils.logger import StructuredLogger
from src.data.topic_data import MBTI_TYPES


def main():
    """Execute weekly fortune publishing for all MBTI types."""
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
    print("Weekly Fortune Publishing System")
    print("MBTI 16 Types x Weekly Forecast -> WordPress")
    print("="*60 + "\n")

    # Check if today is Monday
    today = datetime.now()
    if today.weekday() != 0:
        print(f"Today is {today.strftime('%A')} - Weekly fortunes publish on Mondays only")
        return 0

    try:
        # Initialize generators
        fortune_gen = WeeklyFortuneGenerator(logger=logger)
        wp = WordPressPublisher(logger=logger)

        week_start, week_end = fortune_gen.get_week_dates()
        print(f"Week Period: {week_start} ~ {week_end}\n")

        published_count = 0
        skipped_count = 0

        # Generate and publish for each MBTI type
        for idx, mbti in enumerate(MBTI_TYPES, 1):
            print(f"\n[{idx}/16] Processing {mbti} weekly fortune...")

            # Check if already published for this week
            if db.is_weekly_fortune_published(mbti, week_start):
                print(f"  [SKIP] {mbti} weekly fortune already published for this week")
                skipped_count += 1
                continue

            # Generate content
            print(f"  Generating content...")
            result = fortune_gen.generate_weekly_fortune(mbti)

            print(f"  Title: {result['title'][:50]}...")
            print(f"  Content length: {len(result['content'])} characters")

            # Convert to HTML
            metadata = result.get('metadata')
            html_content = wp.format_content_html(
                result['content'],
                title=result['title'],
                metadata=metadata
            )

            # Prepare categories and tags
            categories = []
            tags = []

            try:
                cat_id = wp.get_or_create_category(f"MBTI {mbti}")
                if cat_id:
                    categories.append(cat_id)

                tag_weekly = wp.get_or_create_tag("주간운세")
                tag_mbti = wp.get_or_create_tag(mbti)

                if tag_weekly:
                    tags.append(tag_weekly)
                if tag_mbti:
                    tags.append(tag_mbti)

            except Exception as e:
                print(f"  [WARN] Category/tag creation failed: {e}")

            # Publish immediately on Monday morning
            status = os.getenv("WORDPRESS_STATUS", "publish")

            publish_result = wp.publish_post(
                title=result['title'],
                content=html_content,
                status=status,
                categories=categories,
                tags=tags,
                metadata=metadata
            )

            print(f"  Published!")
            print(f"  Post ID: {publish_result['post_id']}")
            print(f"  URL: {publish_result['url']}")

            # Save to database
            db.save_weekly_fortune(
                mbti=mbti,
                week_start=week_start,
                week_end=week_end,
                title=result['title'],
                post_id=publish_result['post_id'],
                post_url=publish_result['url'],
                status=publish_result['status']
            )

            published_count += 1

        print("\n" + "="*60)
        print(f"Weekly Fortune Publishing Completed!")
        print(f"Published: {published_count}, Skipped: {skipped_count}")
        print("="*60 + "\n")

        return 0

    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        logger.error(f"Weekly fortune pipeline failed: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
