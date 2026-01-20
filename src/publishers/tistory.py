"""Tistory Open API publisher."""

import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential


class TistoryPublisher:
    """Publish content to Tistory via Open API."""

    def __init__(self, access_token=None, blog_name=None, logger=None):
        """Initialize Tistory publisher.

        Args:
            access_token: Tistory OAuth access token
            blog_name: Tistory blog name (e.g., 'myblog')
            logger: Logger instance
        """
        self.access_token = access_token or os.getenv("TISTORY_ACCESS_TOKEN")
        self.blog_name = blog_name or os.getenv("TISTORY_BLOG_NAME")
        self.logger = logger

        if not self.access_token or not self.blog_name:
            raise ValueError("TISTORY_ACCESS_TOKEN and TISTORY_BLOG_NAME are required")

        self.api_url = "https://www.tistory.com/apis/post/write"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def publish_post(self, title, content, visibility=0, category=None, tag=None):
        """Publish post to Tistory.

        Args:
            title: Post title
            content: Post content (HTML or Markdown)
            visibility: 0=비공개(default), 1=보호, 3=공개
            category: Category ID (optional)
            tag: Comma-separated tags (optional)

        Returns:
            Dict with post_id, url, status
        """
        params = {
            "access_token": self.access_token,
            "output": "json",
            "blogName": self.blog_name,
            "title": title,
            "content": content,
            "visibility": visibility
        }

        if category:
            params["category"] = category

        if tag:
            params["tag"] = tag

        try:
            response = requests.post(
                self.api_url,
                data=params,
                timeout=30
            )

            response.raise_for_status()
            result = response.json()

            if result.get("tistory", {}).get("status") == "200":
                post_data = result["tistory"]
                post_id = post_data.get("postId")
                post_url = post_data.get("url")

                if self.logger:
                    self.logger.info("Post published to Tistory",
                                   post_id=post_id,
                                   url=post_url)

                return {
                    "post_id": post_id,
                    "url": post_url,
                    "status": "published"
                }
            else:
                error_msg = result.get("tistory", {}).get("error_message", "Unknown error")
                raise Exception(f"Tistory API error: {error_msg}")

        except requests.exceptions.RequestException as e:
            if self.logger:
                self.logger.error(f"Tistory publish failed: {str(e)}")
            raise

    def get_category_list(self):
        """Get category list from Tistory.

        Returns:
            List of categories with id, name, parent
        """
        url = "https://www.tistory.com/apis/category/list"
        params = {
            "access_token": self.access_token,
            "output": "json",
            "blogName": self.blog_name
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            result = response.json()

            if result.get("tistory", {}).get("status") == "200":
                categories = result["tistory"]["item"]["categories"]
                return categories
            else:
                return []

        except Exception as e:
            if self.logger:
                self.logger.warning(f"Failed to get categories: {e}")
            return []

    def format_content_html(self, content):
        """Convert markdown-style content to HTML for Tistory.

        Args:
            content: Content with markdown headers

        Returns:
            HTML formatted content
        """
        lines = content.split('\n')
        html_lines = []

        for line in lines:
            # Convert H2 (##)
            if line.startswith('## '):
                text = line.replace('## ', '').strip()
                html_lines.append(f'<h2>{text}</h2>')
            # Convert H3 (###)
            elif line.startswith('### '):
                text = line.replace('### ', '').strip()
                html_lines.append(f'<h3>{text}</h3>')
            # Regular paragraph
            elif line.strip():
                html_lines.append(f'<p>{line}</p>')
            # Empty line
            else:
                html_lines.append('<br>')

        return '\n'.join(html_lines)
