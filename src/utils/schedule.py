"""Schedule utilities for future posting."""

from datetime import datetime, timedelta
import random


def get_next_publish_time():
    """Get next scheduled publish time with random minutes (10:00-10:59 AM or 6:00-6:59 PM KST).

    Returns:
        ISO format datetime string for WordPress
    """
    now = datetime.now()

    # Target times (KST): 10:00-10:59, 18:00-18:59
    target_times = [10, 14, 18]  # 10 AM, 2 PM, 6 PM

    # Generate random minute (0-59) for time distribution
    random_minute = random.randint(0, 59)

    # Find next target time
    next_time = None
    for hour in target_times:
        target = now.replace(hour=hour, minute=random_minute, second=0, microsecond=0)

        # If target time is in the future today
        if target > now:
            next_time = target
            break

    # If no time found today, use tomorrow's 10 AM with random minute
    if next_time is None:
        next_time = (now + timedelta(days=1)).replace(hour=10, minute=random_minute, second=0, microsecond=0)

    # Convert to ISO format for WordPress
    return next_time.isoformat()


def should_schedule():
    """Check if current time requires scheduling (outside publish hours).

    Returns:
        True if should schedule for future, False if should publish now
    """
    now = datetime.now()
    current_hour = now.hour

    # Publish immediately if within target hours (9-11 AM, 1-3 PM, 5-7 PM)
    if (9 <= current_hour < 11) or (13 <= current_hour < 15) or (17 <= current_hour < 19):
        return False

    # Otherwise schedule for next target time (10 AM, 2 PM, or 6 PM with random minutes)
    return True
