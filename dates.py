
from datetime import datetime


def current_utc_iso() -> str:
    return datetime.utcnow().isoformat()
