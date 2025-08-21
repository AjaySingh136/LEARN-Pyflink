#!/usr/bin/env bash
set -euo pipefail

if [ $# -lt 1 ]; then
  echo "Usage: $0 <path-to-python-job> [job-args...]"
  exit 1
fi

JOB_PATH="$1"
shift || true

echo "Submitting $JOB_PATH ..."
docker compose exec -T jobmanager flink run -py "/opt/${JOB_PATH}" "$@"