"""Content validation for safety and quality checks."""

from typing import Dict, List, Tuple
import re

from src.data.topic_data import FORBIDDEN_WORDS
from src.utils.logger import StructuredLogger


class ContentValidator:
    """Validates content for safety, SEO, and quality standards."""

    def __init__(self, logger: StructuredLogger):
        """Initialize validator.

        Args:
            logger: Logger instance
        """
        self.logger = logger
        self.forbidden_words = FORBIDDEN_WORDS
        self.required_disclaimer = "참고 자료일 뿐"

    def validate(self, title: str, content: str) -> Tuple[bool, List[str]]:
        """Validate content against all rules.

        Args:
            title: Post title
            content: Post content

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        # Check for forbidden words
        forbidden_found = self._check_forbidden_words(title + " " + content)
        if forbidden_found:
            issues.append(f"Found forbidden words: {', '.join(forbidden_found)}")

        # Check disclaimer presence
        if not self._check_disclaimer(content):
            issues.append("Missing required disclaimer")

        # Check SEO structure
        if not self._check_seo_structure(content):
            issues.append("Missing proper H2/H3 heading structure")

        # Check minimum length
        if len(content) < 1000:
            issues.append(f"Content too short: {len(content)} characters (minimum 1000)")

        # Log results
        is_valid = len(issues) == 0

        if is_valid:
            self.logger.info("Content validation passed", title=title)
        else:
            self.logger.warning(
                "Content validation failed",
                title=title,
                issues=issues
            )

        return is_valid, issues

    def _check_forbidden_words(self, text: str) -> List[str]:
        """Check for forbidden predictive/certainty words.

        Args:
            text: Text to check

        Returns:
            List of forbidden words found
        """
        found = []
        text_lower = text.lower()

        for word in self.forbidden_words:
            if word.lower() in text_lower:
                found.append(word)

        return found

    def _check_disclaimer(self, content: str) -> bool:
        """Check if required disclaimer is present.

        Args:
            content: Post content

        Returns:
            True if disclaimer is present
        """
        return self.required_disclaimer in content

    def _check_seo_structure(self, content: str) -> bool:
        """Check if content has proper H2/H3 structure.

        Args:
            content: Post content

        Returns:
            True if proper heading structure exists
        """
        # Check for H2 headings (## in markdown)
        h2_pattern = r'^##\s+.+$'
        h2_matches = re.findall(h2_pattern, content, re.MULTILINE)

        # Should have at least 3 H2 sections
        return len(h2_matches) >= 3

    def sanitize_content(self, content: str) -> str:
        """Attempt to sanitize content by removing forbidden words.

        Args:
            content: Original content

        Returns:
            Sanitized content
        """
        sanitized = content

        # Replace forbidden words with softer alternatives
        replacements = {
            "definitely": "likely",
            "guaranteed": "possible",
            "100%": "highly",
            "must happen": "may happen",
            "will happen": "might happen",
            "certain": "probable",
            "확실히": "아마도",
            "반드시": "가능하면",
            "틀림없이": "그럴 수 있습니다",
            "보장": "가능성",
            "무조건": "경우에 따라"
        }

        for forbidden, replacement in replacements.items():
            # Case-insensitive replacement
            pattern = re.compile(re.escape(forbidden), re.IGNORECASE)
            sanitized = pattern.sub(replacement, sanitized)

        self.logger.info("Content sanitized", original_length=len(content), sanitized_length=len(sanitized))

        return sanitized
