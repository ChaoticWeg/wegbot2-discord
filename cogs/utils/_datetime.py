from datetime import datetime, timedelta

def earliest_message():
    return datetime.utcnow() - timedelta(days=14)
