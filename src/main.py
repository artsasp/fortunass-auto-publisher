"""Main orchestrator for content publishing."""

import os
import sys
from dotenv import load_dotenv

from src.generators.topic_generator import TopicGenerator
from src.generators.content_generator import ContentGenerator
from src.validators.seo_validator import SEOValidator
from src.publishers.wordpress import WordPressPublisher
from src.utils.database import TopicDatabase
from src.utils.logger import StructuredLogger


def main():
    """Execute content publishing pipeline."""
    # Load environment
    load_dotenv()

    # Initialize
    logger = StructuredLogger()
    db = TopicDatabase()

    logger.info("=== Content Publishing Pipeline Started ===")

    try:
        # Step 1: Generate unique topic
        logger.info("Step 1: Generating unique topic")
        topic_gen = TopicGenerator(db, logger)
        topic = topic_gen.generate_unique_topic()

        logger.info("Topic generated",
                   mbti=topic['mbti'],
                   love=topic['love_situation'],
                   tarot=topic['tarot_card'])

        # Step 2: Generate content with Claude
        logger.info("Step 2: Generating content with Claude API")
        content_gen = ContentGenerator(logger=logger)
        result = content_gen.generate_content(topic)

        logger.info("Content generated",
                   title=result['title'],
                   length=len(result['content']))

        # Step 3: Validate SEO
        logger.info("Step 3: Validating SEO and safety")
        validator = SEOValidator(logger)
        is_valid, issues = validator.validate(result['title'], result['content'])

        if not is_valid:
            logger.warning("Validation issues found", issues=issues)
            # Auto-fix if possible
            result['content'] = validator.sanitize_content(result['content'])

        # Step 4: Publish to WordPress
        logger.info("Step 4: Publishing to WordPress")
        wp = WordPressPublisher(logger=logger)

        # Get categories and tags
        categories = []
        tags = []

        try:
            cat_id = wp.get_or_create_category(f"MBTI {topic['mbti']}")
            categories.append(cat_id)

            tag_mbti = wp.get_or_create_tag(topic['mbti'])
            tag_tarot = wp.get_or_create_tag(topic['tarot_card'])
            tags = [tag_mbti, tag_tarot]
        except Exception as e:
            logger.warning(f"Failed to create categories/tags: {e}")

        # Publish
        publish_result = wp.publish_post(
            title=result['title'],
            content=result['content'],
            status=os.getenv('PUBLISH_STATUS', 'draft'),
            categories=categories,
            tags=tags
        )

        # Step 5: Save to database
        logger.info("Step 5: Saving to database")
        db.save_published_topic(
            mbti=topic['mbti'],
            love_situation=topic['love_situation'],
            tarot_card=topic['tarot_card'],
            title=result['title'],
            post_id=publish_result.get('post_id'),
            post_url=publish_result.get('link'),
            status=publish_result.get('status')
        )

        logger.info("=== Pipeline Completed Successfully ===",
                   post_id=publish_result.get('post_id'),
                   url=publish_result.get('link'))

        return 0

    except Exception as e:
        logger.error(f"Pipeline failed: {str(e)}", error_type=type(e).__name__)
        return 1


if __name__ == "__main__":
    sys.exit(main())
