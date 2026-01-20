"""Logging configuration and utilities."""

import logging
import os
import json
from datetime import datetime
from typing import Any, Dict


class StructuredLogger:
    """JSON-structured logger for monitoring and debugging."""

    def __init__(self, name: str = "content_publisher", log_dir: str = "logs"):
        """Initialize logger.

        Args:
            name: Logger name
            log_dir: Directory for log files
        """
        self.name = name
        self.log_dir = log_dir
        os.makedirs(log_dir, exist_ok=True)

        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Prevent duplicate handlers
        if self.logger.handlers:
            return

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

        # File handler (JSON format)
        log_file = os.path.join(
            log_dir,
            f"{datetime.now().strftime('%Y-%m-%d')}.log"
        )
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        self.logger.addHandler(file_handler)

    def info(self, message: str, **kwargs):
        """Log info level message with structured data."""
        self._log('INFO', message, kwargs)

    def error(self, message: str, **kwargs):
        """Log error level message with structured data."""
        self._log('ERROR', message, kwargs)

    def warning(self, message: str, **kwargs):
        """Log warning level message with structured data."""
        self._log('WARNING', message, kwargs)

    def _log(self, level: str, message: str, data: Dict[str, Any]):
        """Internal log method with JSON structure."""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message,
            **data
        }

        # Console output (human-readable)
        if level == 'INFO':
            self.logger.info(message)
        elif level == 'ERROR':
            self.logger.error(message)
        elif level == 'WARNING':
            self.logger.warning(message)

        # File output (JSON)
        log_file = os.path.join(
            self.log_dir,
            f"{datetime.now().strftime('%Y-%m-%d')}.log"
        )
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

    def log_pipeline_start(self):
        """Log pipeline execution start."""
        self.info("=" * 50)
        self.info("Content publishing pipeline started")
        self.info("=" * 50)

    def log_pipeline_end(self, success: bool, **kwargs):
        """Log pipeline execution end."""
        status = "SUCCESS" if success else "FAILED"
        self.info("=" * 50)
        self.info(f"Content publishing pipeline {status}", **kwargs)
        self.info("=" * 50)
