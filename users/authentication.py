# token checker if token expired or not
from datetime import timedelta, datetime

import pytz
from django.conf import settings


def is_token_expired(token):
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    return token.created < utc_now - timedelta(days=settings.TOKEN_EXPIRED_AFTER_DAYS)
