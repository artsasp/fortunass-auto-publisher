"""WordPress REST API publisher."""

import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential


class WordPressPublisher:
    """Publish content to WordPress via REST API."""

    def __init__(self, url=None, username=None, app_password=None, logger=None):
        """Initialize WordPress publisher.

        Args:
            url: WordPress site URL (e.g., https://example.com)
            username: WordPress username
            app_password: WordPress application password
            logger: Logger instance
        """
        self.url = (url or os.getenv("WORDPRESS_URL", "")).rstrip("/")
        self.username = username or os.getenv("WORDPRESS_USERNAME")
        self.app_password = app_password or os.getenv("WORDPRESS_APP_PASSWORD")
        self.logger = logger

        if not all([self.url, self.username, self.app_password]):
            raise ValueError("WORDPRESS_URL, WORDPRESS_USERNAME, and WORDPRESS_APP_PASSWORD are required")

        self.api_url = f"{self.url}/wp-json/wp/v2"
        self.auth = (self.username, self.app_password)

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def publish_post(self, title, content, status="draft", categories=None, tags=None, scheduled_date=None, metadata=None):
        """Publish post to WordPress.

        Args:
            title: Post title
            content: Post content (HTML or plain text)
            status: Post status (draft, publish, pending, private, future)
            categories: List of category IDs
            tags: List of tag IDs
            scheduled_date: ISO format datetime for future posts (e.g., "2026-01-17T10:00:00")
            metadata: Dict with SEO metadata (meta_description, og_title, og_description)

        Returns:
            Dict with post_id, url, status
        """
        endpoint = f"{self.api_url}/posts"

        post_data = {
            "title": title,
            "content": content,
            "status": status
        }

        if categories:
            post_data["categories"] = categories
        if tags:
            post_data["tags"] = tags
        if scheduled_date:
            post_data["date"] = scheduled_date

        try:
            response = requests.post(
                endpoint,
                json=post_data,
                auth=self.auth,
                timeout=30
            )

            response.raise_for_status()
            result = response.json()

            if self.logger:
                self.logger.info("Post published to WordPress",
                               post_id=result["id"],
                               status=result["status"])

            post_id = result["id"]

            # Update SEO meta fields if metadata provided
            if metadata:
                self._update_seo_meta(post_id, metadata)

            return {
                "post_id": post_id,
                "url": result["link"],
                "status": result["status"]
            }

        except requests.exceptions.RequestException as e:
            if self.logger:
                self.logger.error(f"WordPress publish failed: {str(e)}")

            # Fallback to draft
            if status != "draft":
                if self.logger:
                    self.logger.info("Retrying as draft")
                post_data["status"] = "draft"

                try:
                    response = requests.post(
                        endpoint,
                        json=post_data,
                        auth=self.auth,
                        timeout=30
                    )
                    response.raise_for_status()
                    result = response.json()

                    return {
                        "post_id": result["id"],
                        "url": result["link"],
                        "status": "draft"
                    }
                except:
                    raise e
            else:
                raise

    def get_or_create_category(self, name):
        """Get category ID by name or create if not exists.

        Args:
            name: Category name

        Returns:
            Category ID or None
        """
        endpoint = f"{self.api_url}/categories"

        try:
            # Search for existing
            response = requests.get(
                endpoint,
                params={"search": name},
                auth=self.auth,
                timeout=10
            )

            if response.ok:
                categories = response.json()
                if categories:
                    return categories[0]["id"]

            # Create new
            response = requests.post(
                endpoint,
                json={"name": name},
                auth=self.auth,
                timeout=10
            )

            if response.ok:
                return response.json()["id"]

        except Exception as e:
            if self.logger:
                self.logger.warning(f"Category operation failed: {e}")

        return None

    def get_or_create_tag(self, name):
        """Get tag ID by name or create if not exists.

        Args:
            name: Tag name

        Returns:
            Tag ID or None
        """
        endpoint = f"{self.api_url}/tags"

        try:
            # Search for existing
            response = requests.get(
                endpoint,
                params={"search": name},
                auth=self.auth,
                timeout=10
            )

            if response.ok:
                tags = response.json()
                if tags:
                    return tags[0]["id"]

            # Create new
            response = requests.post(
                endpoint,
                json={"name": name},
                auth=self.auth,
                timeout=10
            )

            if response.ok:
                return response.json()["id"]

        except Exception as e:
            if self.logger:
                self.logger.warning(f"Tag operation failed: {e}")

        return None

    def format_content_html(self, content, title="", metadata=None):
        """Convert markdown-style content to HTML for WordPress.

        Args:
            content: Content with markdown headers
            title: Post title for schema
            metadata: SEO metadata dict

        Returns:
            HTML formatted content with JSON-LD schema
        """
        lines = content.split('\n')
        html_lines = []

        # Note: JSON-LD schema commented out as WordPress may block script tags via REST API
        # Add it via a plugin like Yoast SEO or Rank Math instead
        # if title and metadata:
        #     schema = self._generate_json_ld_schema(title, metadata)
        #     html_lines.append(schema)
        #     html_lines.append('')

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
            # Empty line - add line break
            else:
                html_lines.append('')

        return '\n'.join(html_lines)

    def _generate_json_ld_schema(self, title, metadata):
        """Generate JSON-LD Article schema markup.

        Args:
            title: Post title
            metadata: Dict with meta_description, og_title, etc.

        Returns:
            JSON-LD script tag
        """
        import json
        from datetime import datetime

        schema = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "description": metadata.get('meta_description', ''),
            "author": {
                "@type": "Organization",
                "name": "Fortune Tarot"
            },
            "publisher": {
                "@type": "Organization",
                "name": "Fortune Tarot",
                "logo": {
                    "@type": "ImageObject",
                    "url": f"{self.url}/wp-content/uploads/logo.png"
                }
            },
            "datePublished": datetime.now().isoformat(),
            "dateModified": datetime.now().isoformat()
        }

        json_str = json.dumps(schema, ensure_ascii=False, indent=2)
        return f'<script type="application/ld+json">\n{json_str}\n</script>'

    def upload_image(self, image_data, filename="featured-image.jpg", alt_text=""):
        """Upload image to WordPress media library.

        Args:
            image_data: Image binary data
            filename: Filename for the image
            alt_text: Alt text for accessibility

        Returns:
            Media ID or None
        """
        endpoint = f"{self.api_url}/media"

        try:
            headers = {
                "Content-Disposition": f'attachment; filename="{filename}"',
                "Content-Type": "image/jpeg"
            }

            response = requests.post(
                endpoint,
                headers=headers,
                data=image_data,
                auth=self.auth,
                timeout=60
            )

            response.raise_for_status()
            result = response.json()

            media_id = result["id"]

            # Set alt text
            if alt_text:
                alt_endpoint = f"{self.api_url}/media/{media_id}"
                requests.post(
                    alt_endpoint,
                    json={"alt_text": alt_text},
                    auth=self.auth,
                    timeout=10
                )

            if self.logger:
                self.logger.info("Image uploaded to WordPress", media_id=media_id)

            return media_id

        except Exception as e:
            if self.logger:
                self.logger.warning(f"Image upload failed: {e}")
            return None

    def set_featured_image(self, post_id, media_id):
        """Set featured image for a post.

        Args:
            post_id: WordPress post ID
            media_id: Media library image ID

        Returns:
            True if successful
        """
        endpoint = f"{self.api_url}/posts/{post_id}"

        try:
            response = requests.post(
                endpoint,
                json={"featured_media": media_id},
                auth=self.auth,
                timeout=10
            )

            response.raise_for_status()

            if self.logger:
                self.logger.info("Featured image set", post_id=post_id, media_id=media_id)

            return True

        except Exception as e:
            if self.logger:
                self.logger.warning(f"Failed to set featured image: {e}")
            return False

    def _update_seo_meta(self, post_id, metadata):
        """Update SEO meta fields for Yoast SEO and Rank Math.

        Args:
            post_id: WordPress post ID
            metadata: Dict with meta_description, og_title, og_description
        """
        endpoint = f"{self.api_url}/posts/{post_id}"

        # First, try to set excerpt (used by many themes as meta description)
        try:
            if metadata.get('meta_description'):
                response = requests.post(
                    endpoint,
                    json={"excerpt": metadata['meta_description']},
                    auth=self.auth,
                    timeout=10
                )
                if response.ok and self.logger:
                    self.logger.info("Excerpt updated", post_id=post_id)
        except Exception as e:
            if self.logger:
                self.logger.warning(f"Failed to update excerpt: {e}")

        # Then try to set SEO plugin meta fields (may not work without plugins)
        meta_fields = {}

        # Yoast SEO meta fields
        if metadata.get('meta_description'):
            meta_fields['_yoast_wpseo_metadesc'] = metadata['meta_description']

        if metadata.get('og_title'):
            meta_fields['_yoast_wpseo_opengraph-title'] = metadata['og_title']
            meta_fields['_yoast_wpseo_twitter-title'] = metadata['og_title']

        if metadata.get('og_description'):
            meta_fields['_yoast_wpseo_opengraph-description'] = metadata['og_description']
            meta_fields['_yoast_wpseo_twitter-description'] = metadata['og_description']

        # Rank Math meta fields (fallback)
        if metadata.get('meta_description'):
            meta_fields['rank_math_description'] = metadata['meta_description']

        if metadata.get('og_title'):
            meta_fields['rank_math_facebook_title'] = metadata['og_title']
            meta_fields['rank_math_twitter_title'] = metadata['og_title']

        if metadata.get('og_description'):
            meta_fields['rank_math_facebook_description'] = metadata['og_description']
            meta_fields['rank_math_twitter_description'] = metadata['og_description']

        if meta_fields:
            try:
                response = requests.post(
                    endpoint,
                    json={"meta": meta_fields},
                    auth=self.auth,
                    timeout=10
                )

                if response.ok and self.logger:
                    self.logger.info("SEO meta fields updated", post_id=post_id)

            except Exception as e:
                if self.logger:
                    self.logger.warning(f"Failed to update SEO meta: {e}")
