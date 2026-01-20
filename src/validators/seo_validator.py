"""SEO and content safety validator."""

import re
from src.data.topic_data import FORBIDDEN_WORDS


class SEOValidator:
    """Validate content for SEO and safety."""

    def __init__(self, logger=None):
        """Initialize validator."""
        self.logger = logger
        self.forbidden_words = FORBIDDEN_WORDS
        self.required_disclaimer_keywords = ["참고 자료", "선택과 책임", "본인에게"]

    def validate(self, title, content):
        """Validate title and content.

        Args:
            title: Post title
            content: Post content

        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []

        # Check forbidden words
        forbidden_found = self._check_forbidden_words(title + " " + content)
        if forbidden_found:
            issues.append(f"Forbidden words: {', '.join(forbidden_found[:3])}")

        # Check disclaimer
        if not self._check_disclaimer(content):
            issues.append("Missing disclaimer")

        # Check headings
        if not self._check_headings(content):
            issues.append("Missing H2 headings")

        # Check length
        if len(content) < 1000:
            issues.append(f"Too short: {len(content)} chars")

        is_valid = len(issues) == 0

        if self.logger:
            if is_valid:
                self.logger.info("Validation passed")
            else:
                self.logger.warning("Validation issues", issues=issues)

        return is_valid, issues

    def _check_forbidden_words(self, text):
        """Check for forbidden words."""
        found = []
        text_lower = text.lower()

        for word in self.forbidden_words:
            if word.lower() in text_lower:
                found.append(word)

        return found

    def _check_disclaimer(self, content):
        """Check if disclaimer exists."""
        # Check if all key disclaimer words are present
        return all(keyword in content for keyword in self.required_disclaimer_keywords)

    def _check_headings(self, content):
        """Check for H2 headings."""
        h2_pattern = r'^##\s+.+$'
        matches = re.findall(h2_pattern, content, re.MULTILINE)
        return len(matches) >= 3

    def sanitize_content(self, content):
        """Remove or replace forbidden words."""
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

        sanitized = content

        for forbidden, replacement in replacements.items():
            pattern = re.compile(re.escape(forbidden), re.IGNORECASE)
            sanitized = pattern.sub(replacement, sanitized)

        if self.logger:
            self.logger.info("Content sanitized")

        return sanitized
