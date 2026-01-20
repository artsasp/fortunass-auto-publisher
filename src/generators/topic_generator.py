"""Topic generator with duplicate prevention."""

import random
from typing import Dict, Tuple

from src.data.topic_data import (
    MBTI_TYPES, LOVE_SITUATIONS, CARD_TYPES,
    TAROT_MAJOR_ARCANA, TAROT_KOREAN,
    NUMEROLOGY_NUMBERS, NUMEROLOGY_KOREAN,
    ORACLE_CARDS, ORACLE_KOREAN
)
from src.utils.database import TopicDatabase
from src.utils.logger import StructuredLogger


class TopicGenerator:
    """Generates unique topic combinations for content creation."""

    def __init__(self, db: TopicDatabase, logger: StructuredLogger):
        """Initialize topic generator.

        Args:
            db: Database instance for duplicate checking
            logger: Logger instance
        """
        self.db = db
        self.logger = logger
        self.max_attempts = 100

    def generate_unique_topic(self) -> Dict[str, str]:
        """Generate a unique topic combination with random card type.

        Returns:
            Dictionary with mbti, love_situation, card_type, card_name, card_korean

        Raises:
            RuntimeError: If unable to generate unique topic after max_attempts
        """
        self.logger.info("Starting topic generation")

        for attempt in range(self.max_attempts):
            # Random selection
            mbti = random.choice(MBTI_TYPES)
            love_situation = random.choice(LOVE_SITUATIONS)
            card_type = random.choice(CARD_TYPES)

            # Select card based on type
            if card_type == "tarot":
                card_name = random.choice(TAROT_MAJOR_ARCANA)
                card_korean = TAROT_KOREAN[card_name]
            elif card_type == "numerology":
                card_name = random.choice(NUMEROLOGY_NUMBERS)
                card_korean = NUMEROLOGY_KOREAN[card_name]
            else:  # oracle
                card_name = random.choice(ORACLE_CARDS)
                card_korean = ORACLE_KOREAN[card_name]

            # Check if combination already used
            if not self.db.is_topic_used(mbti, love_situation, card_name):
                topic = {
                    'mbti': mbti,
                    'love_situation': love_situation,
                    'card_type': card_type,
                    'card_name': card_name,
                    'card_korean': card_korean,
                    # Legacy fields for compatibility
                    'tarot_card': card_name,
                    'tarot_korean': card_korean
                }

                self.logger.info(
                    "Generated unique topic",
                    mbti=mbti,
                    love_situation=love_situation,
                    card_type=card_type,
                    card_name=card_name,
                    attempt=attempt + 1
                )

                return topic

        # Failed to generate unique topic
        self.logger.error(
            "Failed to generate unique topic",
            max_attempts=self.max_attempts
        )
        raise RuntimeError(
            f"Unable to generate unique topic after {self.max_attempts} attempts. "
            "Database may be exhausted."
        )

    def calculate_remaining_combinations(self) -> int:
        """Calculate how many topic combinations are still available.

        Returns:
            Number of remaining unique combinations
        """
        total_possible = len(MBTI_TYPES) * len(LOVE_SITUATIONS) * len(TAROT_MAJOR_ARCANA)
        stats = self.db.get_stats()
        used = stats['total_published']
        remaining = total_possible - used

        self.logger.info(
            "Topic pool status",
            total_possible=total_possible,
            used=used,
            remaining=remaining,
            utilization_percent=round(used / total_possible * 100, 2)
        )

        return remaining
