#!/bin/bash

if [[ $# -ne 2 ]]; then
    echo "Usage: $0 'https://target.com/page?q=' payloads.txt"
    exit 1
fi

TARGET=$1
PAYLOADS=$2

echo "[*] Testing XSS payloads on: $TARGET"
echo "[*] Payload list: $PAYLOADS"
echo

while read -r payload; do
    ENCODED=$(printf "$payload" | jq -sRr @uri)
    FULL_URL="${TARGET}${ENCODED}"
    RESPONSE=$(curl -sk "$FULL_URL" --max-time 10)

    if echo "$RESPONSE" | grep -q "$payload"; then
        echo "[✅] Potential XSS with payload: $payload"
    else
        echo "[❌] Not reflected: $payload"
    fi
done < "$PAYLOADS"
