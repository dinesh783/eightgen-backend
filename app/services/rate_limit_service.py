import logging
import time
from collections import defaultdict

from fastapi import HTTPException, status

from app.models import Partner


logger = logging.getLogger("app.services.ratelimit")


class RateLimitService:
    # {partner_id: {minute_ts: count}}
    _state: dict[int, dict[int, int]] = defaultdict(lambda: defaultdict(int))

    def enforce(self, partner: Partner) -> None:
        current_minute = int(time.time() // 60)
        used = self._state[partner.id][current_minute]

        if used >= partner.rate_limit_per_minute:
            logger.warning(
                "Rate limit exceeded for partner_id=%s used=%s limit=%s",
                partner.id,
                used,
                partner.rate_limit_per_minute,
            )
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded",
            )

        self._state[partner.id][current_minute] += 1
