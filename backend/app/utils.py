from datetime import datetime, timedelta, timezone

def get_wita_now():
    return datetime.now(timezone(timedelta(hours=8))).replace(tzinfo=None)

def get_wita_today():
    return datetime.now(timezone(timedelta(hours=8))).date()
