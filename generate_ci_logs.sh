#!/bin/bash

ED_URL="http://6ebf4e82-073c-426b-9f56-f9b1915c6ab1-http-us-west2-cf.aws.edgedelta.com"

BRANCHES=("main" "dev" "feature/login" "hotfix/payment")
STATUSES=("passed" "failed" "errored")

echo "Sending NEW synthetic CircleCI logs to:"
echo "  $ED_URL"
echo

for i in $(seq 1 80); do
  BRANCH=${BRANCHES[$(( RANDOM % ${#BRANCHES[@]} ))]}
  STATUS=${STATUSES[$(( RANDOM % ${#STATUSES[@]} ))]}

  # Random duration between 10 and 300 seconds
  DURATION=$(awk -v min=10 -v max=300 'BEGIN{srand(); print min+rand()*(max-min)}')

  # ISO timestamp
  TS=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

  JSON=$(cat <<EOF2
{
  "job": "synthetic-run-tests",
  "repo": "edge-delta-circle-ci-demo",
  "branch": "$BRANCH",
  "commit": "$(openssl rand -hex 20)",
  "status": "$STATUS",
  "duration_seconds": $DURATION,
  "passed": $((RANDOM % 25)),
  "failed": $((RANDOM % 6)),
  "errors": $((RANDOM % 3)),
  "timestamp": "$TS",
  "raw_logs": "Synthetic CI run #$i with status=$STATUS"
}
EOF2
)

  curl -s -X POST "$ED_URL" \
    -H "Content-Type: application/json" \
    -d "$JSON" > /dev/null

  echo "Sent synthetic log $i – status=$STATUS branch=$BRANCH"
done

echo
echo "Done sending 80 NEW synthetic CI logs."
