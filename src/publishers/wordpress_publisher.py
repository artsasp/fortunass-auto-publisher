"""WordPress publishing with REST API and retry logic."""

import os
import requests
from typing import Optional, Dict, List
from datetime import datetime, timedelta
from tenacity import retry, stop_after_attempt, wait_exponential

from src.utils.logger import StructuredLogger


class WordPressPublisher:
    """Publishes content to WordPress via REST API with robust error handling."""

    def __init__(
        self,
        site_url: str = None,
        username: str = None,
        app_password: str = None,
        logger: StructuredLogger = None
    ):
        """Initialize WordPress publisher.

        Args:
            site_url: WordPress site URL
            username: WordPress username
            app_password: WordPress application password
            logger: Logger instance
        """
        self.site_url = (site_url or os.getenv("WORDPRESS_SITE_URL", "")).rstrip("/")
        self.username = username or os.getenv("WORDPRESS_USERNAME")
        self.app_password = app_password or os.getenv("WORDPRESS_APP_PASSWORD")
        self.logger = logger

        if not all([self.site_url, self.username, self.app_password]):
            raise ValueError(
                "WORDPRESS_SITE_URL, WORDPRESS_USERNAME, and WORDPRESS_APP_PASSWORD must be set"
            )

        self.api_url = f"{self.site_url}/wp-json/wp/v2"
        self.timeout = 30

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    def publish_post(
        self,
        title: str,
        content: str,
        status: str = "draft",
        categories: Optional[List[int]] = None,
        tags: Optional[List[int]] = None,
        schedule_hours: Optional[int] = None
    ) -> Dict[str, any]:
        """Publish post to WordPress.

        Args:
            title: Post title
            content: Post content (HTML or markdown)
            status: Post status (draft, publish, future, pending)
            categories: List of category IDs
            tags: List of tag IDs
            schedule_hours: Hours from now to schedule (for future posts)

        Returns:
            Dictionary with post_id, link, status, and success flag

        Raises:
            Exception: If publishing fails after retries
        """
        self.logger.info(
            "Publishing to WordPress",
            title=title,
            status=status,
            scheduled=schedule_hours is not None
        )

        try:
            endpoint = f"{self.api_url}/posts"

            post_data = {
                "title": title,
                "content": content,
                "status": status
            }

            # Add categories and tags if provided
            if categories:
                post_data["categories"] = categories
            if tags:
                post_data["tags"] = tags

            # Schedule post for future
            if schedule_hours and status == "future":
                scheduled_time = datetime.now() + timedelta(hours=schedule_hours)
                post_data["date"] = scheduled_time.isoformat()

            # Make request
            response = requests.post(
                endpoint,
                json=post_data,
                auth=(self.username, self.app_password),
                timeout=self.timeout
            )

            response.raise_for_status()
            result = response.json()

            self.logger.info(
                "Post published successfully",
                post_id=result["id"],
                link=result["link"],
                status=result["status"]
            )

            return {
                "success": True,
                "post_id": result["id"],
                "link": result["link"],
                "status": result["status"],
                "title": result["title"]["rendered"]
            }

        except requests.exceptions.RequestException as e:
            self.logger.error(
                "WordPress publishing failed",
                error=str(e),
                title=title,
                status=status
            )
            raise

    def publish_with_fallback(
        self,
        title: str,
        content: str,
        preferred_status: str = "publish",
        **kwargs
    ) -> Dict[str, any]:
        """Publish with automatic fallback to draft on failure.

        Args:
            title: Post title
            content: Post content
            preferred_status: Desired status (publish, future, etc.)
            **kwargs: Additional arguments for publish_post

        Returns:
            Dictionary with publishing result
        """
        try:
            # Try to publish with preferred status
            result = self.publish_post(
                title=title,
                content=content,
                status=preferred_status,
                **kwargs
            )
            return result

        except Exception as e:
            self.logger.warning(
                "Failed to publish with preferred status, falling back to draft",
                preferred_status=preferred_status,
                error=str(e)
            )

            # Fallback: save as draft
            try:
                result = self.publish_post(
                    title=title,
                    content=content,
                    status="draft",
                    **kwargs
                )
                result["fallback_used"] = True
                return result

            except Exception as fallback_error:
                self.logger.error(
                    "Failed to save as draft (critical failure)",
                    error=str(fallback_error)
                )
                return {
                    "success": False,
                    "error": str(fallback_error),
                    "title": title
                }

    def get_or_create_category(self, name: str) -> int:
        """Get category ID by name or create if doesn't exist.

        Args:
            name: Category name

        Returns:
            Category ID
        """
        endpoint = f"{self.api_url}/categories"

        # Search for existing category
        response = requests.get(
            endpoint,
            params={"search": name},
            auth=(self.username, self.app_password),
            timeout=self.timeout
        )
        response.raise_for_status()
        categories = response.json()

        if categories:
            return categories[0]["id"]

        # Create new category
        response = requests.post(
            endpoint,
            json={"name": name},
            auth=(self.username, self.app_password),
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()["id"]

    def get_or_create_tag(self, name: str) -> int:
        """Get tag ID by name or create if doesn't exist.

        Args:
            name: Tag name

        Returns:
            Tag ID
        """
        endpoint = f"{self.api_url}/tags"

        # Search for existing tag
        response = requests.get(
            endpoint,
            params={"search": name},
            auth=(self.username, self.app_password),
            timeout=self.timeout
        )
        response.raise_for_status()
        tags = response.json()

        if tags:
            return tags[0]["id"]

        # Create new tag
        response = requests.post(
            endpoint,
            json={"name": name},
            auth=(self.username, self.app_password),
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()["id"]
