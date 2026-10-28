# In-process rate limiting: engineering boundaries

CivicShield AI uses small, per-process request quotas on some API routes. These are suitable for its local **research demonstration**, not production abuse protection.

## Correctness fix

An older implementation cleared **all** client histories when more than 5,000 (socket, bucket) entries accumulated. That permitted exhausted quotas to become usable again after overflow.

The limiter now:

- Keeps at most 5,000 active client/bucket keys per API process.
- Stores monotonic expiry deadlines, retaining active requests regardless of window duration.
- Removes only expired records when the table fills.
- Refuses a new key with HTTP 429 while all existing slots remain active; it never resets an exhausted client's quota to reclaim capacity.
- Returns a coarse `Retry-After` on 429 responses and the standard random `X-Request-ID` for diagnostic correlation.
- Uses the actual socket peer; untrusted `X-Forwarded-For` is deliberately ignored.
- Includes deterministic tests for capacity exhaustion, expired entry recovery, mixed windows, spoofed headers and a real FastAPI route.

## Essential limitations

A proxy may cause many people to share one socket-based quota. Separate API replicas maintain separate counters; requests are not globally rate-limited. An attacker can also exhaust the bounded table so new clients receive 429: this **fails closed but is not an availability guarantee**.

Any public service would need an authorized, reviewed gateway/edge or distributed limiter, shared state, explicit proxy trust, account-based quotas, monitoring, security/privacy review, capacity testing and incident response. The project does not claim to implement those controls.

**No rate-limiting work constitutes disaster prediction validation or authorization for emergency operations.**
