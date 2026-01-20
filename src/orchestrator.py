"""Main orchestrator for automated content publishing pipeline."""

import os
import sys
from typing import Optional

from src.utils.database import TopicDatabase
from src.utils.logger import StructuredLogger
from src.generators.topic_generator import TopicGenerator
from src.generators.content_generator import ContentGenerator
from src.validators.content_validator import ContentValidator
from src.publishers.wordpress_publisher import WordPressPublisher


class ContentPublisher:
    """Orchestrates the complete content publishing pipeline."""

    def __init__(
        self,
        publish_status: str = "draft",
        auto_sanitize: bool = True,
        schedule_hours: Optional[int] = None
    ):
        """Initialize content publisher.

        Args:
            publish_status: WordPress post status (draft, publish, future)
            auto_sanitize: Auto-sanitize forbidden words if found
            schedule_hours: Hours from now to schedule (if status=future)
        """
        # Initialize components
        self.logger = StructuredLogger()
        self.db = TopicDatabase()
        self.topic_generator = TopicGenerator(self.db, self.logger)
        self.content_generator = ContentGenerator(logger=self.logger)
        self.validator = ContentValidator(self.logger)
        self.wordpress = WordPressPublisher(logger=self.logger)

        self.publish_status = publish_status
        self.auto_sanitize = auto_sanitize
        self.schedule_hours = schedule_hours

    def run(self) -> bool:
        """Execute complete publishing pipeline.

        Returns:
            True if successful, False otherwise
        """
        self.logger.log_pipeline_start()

        try:
            # Step 1: Generate unique topic
            self.logger.info("Step 1/5: Generating unique topic")
            topic = self.topic_generator.generate_unique_topic()
            self.topic_generator.calculate_remaining_combinations()

            # Step 2: Generate content with Claude
            self.logger.info("Step 2/5: Generating content with Claude API")
            content_data = self.content_generator.generate_content(topic)
            title = content_data['title']
            content = content_data['content']

            # Step 3: Validate content
            self.logger.info("Step 3/5: Validating content")
            is_valid, issues = self.validator.validate(title, content)

            if not is_valid:
                if self.auto_sanitize:
                    self.logger.info("Auto-sanitizing content")
                    content = self.validator.sanitize_content(content)

                    # Re-validate
                    is_valid, issues = self.validator.validate(title, content)

                if not is_valid:
                    self.logger.error(
                        "Content validation failed",
                        issues=issues
                    )
                    # Still proceed but as draft
                    self.publish_status = "draft"

            # Step 4: Prepare categories and tags
            self.logger.info("Step 4/5: Preparing categories and tags")
            categories = self._get_categories(topic)
            tags = self._get_tags(topic)

            # Step 5: Publish to WordPress
            self.logger.info("Step 5/5: Publishing to WordPress")
            publish_kwargs = {
                "categories": categories,
                "tags": tags
            }

            if self.publish_status == "future" and self.schedule_hours:
                publish_kwargs["schedule_hours"] = self.schedule_hours

            result = self.wordpress.publish_with_fallback(
                title=title,
                content=content,
                preferred_status=self.publish_status,
                **publish_kwargs
            )

            # Step 6: Save to database
            if result.get("success"):
                self.db.save_published_topic(
                    mbti=topic['mbti'],
                    love_situation=topic['love_situation'],
                    tarot_card=topic['tarot_card'],
                    title=title,
                    post_id=result.get('post_id'),
                    post_url=result.get('link'),
                    status=result.get('status')
                )

                self.logger.log_pipeline_end(
                    success=True,
                    post_id=result.get('post_id'),
                    post_url=result.get('link'),
                    status=result.get('status')
                )

                return True
            else:
                # Save failed attempt to database
                self.db.save_published_topic(
                    mbti=topic['mbti'],
                    love_situation=topic['love_situation'],
                    tarot_card=topic['tarot_card'],
                    title=title,
                    status="failed",
                    error_message=result.get('error')
                )

                self.logger.log_pipeline_end(
                    success=False,
                    error=result.get('error')
                )

                return False

        except Exception as e:
            self.logger.error(
                "Pipeline execution failed",
                error=str(e),
                error_type=type(e).__name__
            )
            self.logger.log_pipeline_end(success=False, error=str(e))
            return False

    def _get_categories(self, topic: dict) -> list:
        """Get or create WordPress categories for the post.

        Args:
            topic: Topic dictionary

        Returns:
            List of category IDs
        """
        try:
            categories = []

            # Main category: MBTI
            mbti_cat = self.wordpress.get_or_create_category(f"MBTI {topic['mbti']}")
            categories.append(mbti_cat)

            # General categories
            tarot_cat = self.wordpress.get_or_create_category("타로 심리 해석")
            categories.append(tarot_cat)

            love_cat = self.wordpress.get_or_create_category("연애 심리")
            categories.append(love_cat)

            return categories

        except Exception as e:
            self.logger.warning(f"Failed to set categories: {e}")
            return []

    def _get_tags(self, topic: dict) -> list:
        """Get or create WordPress tags for the post.

        Args:
            topic: Topic dictionary

        Returns:
            List of tag IDs
        """
        try:
            tags = []

            # Add MBTI type as tag
            mbti_tag = self.wordpress.get_or_create_tag(topic['mbti'])
            tags.append(mbti_tag)

            # Add tarot card as tag
            tarot_tag = self.wordpress.get_or_create_tag(topic['tarot_card'])
            tags.append(tarot_tag)

            # Add Korean tarot name
            tarot_kr_tag = self.wordpress.get_or_create_tag(topic['tarot_korean'])
            tags.append(tarot_kr_tag)

            # Extract main keyword from love situation
            love_keyword = topic['love_situation'].split('(')[0].strip()
            love_tag = self.wordpress.get_or_create_tag(love_keyword)
            tags.append(love_tag)

            return tags

        except Exception as e:
            self.logger.warning(f"Failed to set tags: {e}")
            return []

    def get_stats(self) -> dict:
        """Get publishing statistics.

        Returns:
            Statistics dictionary
        """
        return self.db.get_stats()
