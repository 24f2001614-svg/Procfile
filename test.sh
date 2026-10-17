#!/usr/bin/env bash
# Usage: ./test.sh https://your-service.onrender.com/analytics
URL="${1:-http://localhost:8000/analytics}"
KEY="ak_9vlx1da6klbcb65x4ahw1s0u"
BODY='{"events":[{"user":"a","amount":10,"ts":1},{"user":"b","amount":-5,"ts":2},{"user":"a","amount":2.5,"ts":3}]}'

echo "--- No key (expect 401)";    curl -s -o /dev/null -w "%{http_code}\n" -X POST "$URL" -H "Content-Type: application/json" -d "$BODY"
echo "--- Wrong key (expect 401)"; curl -s -o /dev/null -w "%{http_code}\n" -X POST "$URL" -H "Content-Type: application/json" -H "X-API-Key: wrong" -d "$BODY"
echo "--- Valid key (expect total_events 3, unique_users 2, revenue 12.5, top_user a)"
curl -s -X POST "$URL" -H "Content-Type: application/json" -H "X-API-Key: $KEY" -d "$BODY"; echo
