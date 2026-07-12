from datetime import datetime
import re

def format_published_date(date_str: str) -> str:
    """Convert ISO date to 'X days ago' or formatted date."""
    if not date_str:
        return "Recently"
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        now = datetime.now(dt.tzinfo)
        diff = now - dt
        days = diff.days
        if days == 0:
            hours = diff.seconds // 3600
            if hours < 1:
                minutes = diff.seconds // 60
                return f"{minutes}m ago" if minutes > 0 else "Just now"
            return f"{hours}h ago"
        elif days < 7:
            return f"{days}d ago"
        else:
            return dt.strftime("%b %d, %Y")
    except:
        return date_str

def truncate_text(text: str, max_length: int = 120) -> str:
    """Truncate text to max length with ellipsis."""
    if len(text) <= max_length:
        return text
    return text[:max_length].rsplit(" ", 1)[0] + "..."