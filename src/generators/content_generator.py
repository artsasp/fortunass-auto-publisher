"""Content generation using Claude API."""

import os
from anthropic import Anthropic
from tenacity import retry, stop_after_attempt, wait_exponential

from src.generators.prompt_template import get_content_generation_prompt


class ContentGenerator:
    """Generates content using Claude API."""

    def __init__(self, api_key=None, logger=None):
        """Initialize content generator."""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")

        self.client = Anthropic(api_key=self.api_key)
        self.logger = logger
        self.model = "claude-sonnet-4-5-20250929"
        self.max_tokens = 6000  # 증가: 글이 완전히 작성되도록

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def generate_content(self, topic):
        """Generate content for given topic.

        Args:
            topic: Dict with mbti, love_situation, tarot_card, tarot_korean

        Returns:
            Dict with title and content
        """
        if self.logger:
            self.logger.info("Calling Claude API")

        prompt = get_content_generation_prompt(
            mbti=topic['mbti'],
            love_situation=topic['love_situation'],
            tarot_card=topic['tarot_card'],
            tarot_korean=topic['tarot_korean'],
            card_type=topic.get('card_type', 'tarot')
        )

        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text

            # Parse response
            title, content = self._parse_response(response_text)

            if self.logger:
                self.logger.info("Claude API call successful",
                               tokens=message.usage.input_tokens + message.usage.output_tokens)

            # Parse metadata
            metadata = self._parse_metadata(response_text)

            return {
                'title': title,
                'content': content,
                'metadata': metadata
            }

        except Exception as e:
            if self.logger:
                self.logger.error(f"Claude API error: {str(e)}")
            raise

    def _parse_metadata(self, response_text):
        """Parse SEO metadata from response."""
        metadata = {
            'meta_description': '',
            'og_title': '',
            'og_description': '',
            'image_alt': '',
            'internal_links': []
        }

        lines = response_text.split('\n')
        for line in lines:
            if line.startswith('META_DESCRIPTION:'):
                metadata['meta_description'] = line.replace('META_DESCRIPTION:', '').strip()
            elif line.startswith('OG_TITLE:'):
                metadata['og_title'] = line.replace('OG_TITLE:', '').strip()
            elif line.startswith('OG_DESCRIPTION:'):
                metadata['og_description'] = line.replace('OG_DESCRIPTION:', '').strip()
            elif line.startswith('IMAGE_ALT:'):
                metadata['image_alt'] = line.replace('IMAGE_ALT:', '').strip()
            elif line.startswith('INTERNAL_LINKS:'):
                # Will be parsed from content later
                pass

        return metadata

    def _parse_response(self, response_text):
        """Parse title and content from response."""
        # Split by separator to get metadata and content
        parts = response_text.split('---')

        if len(parts) >= 2:
            # Metadata in first part, content in second
            content_part = '---'.join(parts[1:])
        else:
            # No separator, use whole text
            content_part = response_text

        lines = content_part.strip().split('\n')

        title = ""
        content_lines = []
        found_title = False

        for line in lines:
            stripped = line.strip()

            # Find title (first H2 or H1)
            if not found_title and stripped.startswith('#'):
                title = stripped.lstrip('#').strip()
                found_title = True
                continue

            # Collect content after title
            if found_title:
                content_lines.append(line)

        # If no title found, use first non-empty line
        if not title:
            for line in lines:
                if line.strip():
                    title = line.strip()
                    break

        content = '\n'.join(content_lines).strip()

        # Fallback
        if not content:
            content = content_part

        return title, content
