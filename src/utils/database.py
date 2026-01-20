"""SQLite database manager for tracking published topics."""

import sqlite3
import os
from datetime import datetime
from typing import Optional


class TopicDatabase:
    """Manages published topics to prevent duplicates."""

    def __init__(self, db_path: str = "data/published_topics.db"):
        """Initialize database connection.

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    def _init_db(self):
        """Create tables if they don't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS published_topics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mbti TEXT NOT NULL,
                    love_situation TEXT NOT NULL,
                    tarot_card TEXT NOT NULL,
                    title TEXT NOT NULL,
                    post_id INTEGER,
                    post_url TEXT,
                    status TEXT NOT NULL,
                    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    error_message TEXT
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_topic_combination
                ON published_topics(mbti, love_situation, tarot_card)
            """)

            # Weekly fortune table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS weekly_fortunes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    mbti TEXT NOT NULL,
                    week_start TEXT NOT NULL,
                    week_end TEXT NOT NULL,
                    title TEXT NOT NULL,
                    post_id INTEGER,
                    post_url TEXT,
                    status TEXT NOT NULL,
                    published_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    error_message TEXT
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_weekly_fortune
                ON weekly_fortunes(mbti, week_start)
            """)
            conn.commit()

    def is_topic_used(self, mbti: str, love_situation: str, tarot_card: str) -> bool:
        """Check if topic combination has been used.

        Args:
            mbti: MBTI type
            love_situation: Love situation
            tarot_card: Tarot card name

        Returns:
            True if topic has been used before
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM published_topics
                WHERE mbti = ? AND love_situation = ? AND tarot_card = ?
            """, (mbti, love_situation, tarot_card))
            count = cursor.fetchone()[0]
            return count > 0

    def save_published_topic(
        self,
        mbti: str,
        love_situation: str,
        tarot_card: str,
        title: str,
        post_id: Optional[int] = None,
        post_url: Optional[str] = None,
        status: str = "draft",
        error_message: Optional[str] = None
    ):
        """Save published topic to database.

        Args:
            mbti: MBTI type
            love_situation: Love situation
            tarot_card: Tarot card name
            title: Post title
            post_id: WordPress post ID
            post_url: Published post URL
            status: Publication status
            error_message: Error message if failed
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO published_topics
                (mbti, love_situation, tarot_card, title, post_id, post_url, status, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (mbti, love_situation, tarot_card, title, post_id, post_url, status, error_message))
            conn.commit()

    def get_stats(self) -> dict:
        """Get publishing statistics.

        Returns:
            Dictionary with statistics
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()

            # Total published
            cursor.execute("SELECT COUNT(*) FROM published_topics")
            total = cursor.fetchone()[0]

            # By status
            cursor.execute("""
                SELECT status, COUNT(*) FROM published_topics
                GROUP BY status
            """)
            by_status = dict(cursor.fetchall())

            # Success rate
            success_count = by_status.get('publish', 0) + by_status.get('draft', 0)
            success_rate = (success_count / total * 100) if total > 0 else 0

            return {
                'total_published': total,
                'by_status': by_status,
                'success_rate': round(success_rate, 2)
            }

    def is_weekly_fortune_published(self, mbti: str, week_start: str) -> bool:
        """Check if weekly fortune for this MBTI and week has been published.

        Args:
            mbti: MBTI type
            week_start: Week start date (YYYY-MM-DD)

        Returns:
            True if already published
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) FROM weekly_fortunes
                WHERE mbti = ? AND week_start = ?
            """, (mbti, week_start))
            count = cursor.fetchone()[0]
            return count > 0

    def save_weekly_fortune(
        self,
        mbti: str,
        week_start: str,
        week_end: str,
        title: str,
        post_id: Optional[int] = None,
        post_url: Optional[str] = None,
        status: str = "draft",
        error_message: Optional[str] = None
    ):
        """Save published weekly fortune to database.

        Args:
            mbti: MBTI type
            week_start: Week start date
            week_end: Week end date
            title: Post title
            post_id: WordPress post ID
            post_url: Published post URL
            status: Publication status
            error_message: Error message if failed
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO weekly_fortunes
                (mbti, week_start, week_end, title, post_id, post_url, status, error_message)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (mbti, week_start, week_end, title, post_id, post_url, status, error_message))
            conn.commit()
