"""Weekly fortune content generator."""

import os
from datetime import datetime, timedelta
from anthropic import Anthropic
from tenacity import retry, stop_after_attempt, wait_exponential

from src.generators.weekly_fortune_template import get_weekly_fortune_prompt
from src.data.topic_data import MBTI_TYPES


class WeeklyFortuneGenerator:
    """Generates weekly fortune content for all MBTI types."""

    def __init__(self, api_key=None, logger=None):
        """Initialize weekly fortune generator."""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is required")

        self.client = Anthropic(api_key=self.api_key)
        self.logger = logger
        self.model = "claude-sonnet-4-5-20250929"
        self.max_tokens = 6000

    def get_week_dates(self):
        """Get this week's start and end dates (Monday to Sunday).

        Returns:
            Tuple of (week_start, week_end) in YYYY-MM-DD format
        """
        today = datetime.now()
        # Get Monday of current week
        monday = today - timedelta(days=today.weekday())
        # Get Sunday of current week
        sunday = monday + timedelta(days=6)

        return monday.strftime("%Y-%m-%d"), sunday.strftime("%Y-%m-%d")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=10))
    def generate_weekly_fortune(self, mbti: str):
        """Generate weekly fortune for specific MBTI type.

        Args:
            mbti: MBTI personality type

        Returns:
            Dict with title and content
        """
        week_start, week_end = self.get_week_dates()

        if self.logger:
            self.logger.info("Generating weekly fortune", mbti=mbti, week=f"{week_start}~{week_end}")

        prompt = get_weekly_fortune_prompt(mbti, week_start, week_end)

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
            metadata = self._parse_metadata(response_text)

            if self.logger:
                self.logger.info("Weekly fortune generated",
                               mbti=mbti,
                               tokens=message.usage.input_tokens + message.usage.output_tokens)

            return {
                'title': title,
                'content': content,
                'metadata': metadata,
                'mbti': mbti,
                'week_start': week_start,
                'week_end': week_end
            }

        except Exception as e:
            if self.logger:
                self.logger.error(f"Weekly fortune generation failed: {str(e)}")
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

        return metadata

    def _parse_response(self, response_text):
        """Parse title and content from response."""
        # Split by separator to get metadata and content
        parts = response_text.split('---')

        if len(parts) >= 2:
            content_part = '---'.join(parts[1:])
        else:
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

    def generate_all_weekly_fortunes(self):
        """Generate weekly fortunes for all 16 MBTI types.

        Returns:
            List of dicts with weekly fortune data
        """
        fortunes = []

        for mbti in MBTI_TYPES:
            try:
                fortune = self.generate_weekly_fortune(mbti)
                fortunes.append(fortune)

                if self.logger:
                    self.logger.info(f"Generated weekly fortune for {mbti}")

            except Exception as e:
                if self.logger:
                    self.logger.error(f"Failed to generate weekly fortune for {mbti}: {e}")
                continue

        return fortunes
