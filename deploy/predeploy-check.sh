#!/usr/bin/env bash
set -euo pipefail

echo "[1/5] Backend tests"
DJANGO_DEBUG=True uv run pytest

SECRET_VALUE="${SECRET_KEY:-${DJANGO_SECRET_KEY:-}}"
if [[ -z "${SECRET_VALUE}" ]]; then
  echo "ERROR: SECRET_KEY (or DJANGO_SECRET_KEY) is not set."
  exit 1
fi
if [[ "${SECRET_VALUE}" == django-insecure-* ]]; then
  echo "ERROR: SECRET_KEY uses insecure default prefix."
  exit 1
fi
if [[ -z "${DJANGO_ALLOWED_HOSTS:-}" ]]; then
  echo "ERROR: DJANGO_ALLOWED_HOSTS is not set."
  exit 1
fi
if [[ -z "${DJANGO_CSRF_TRUSTED_ORIGINS:-}" ]]; then
  echo "ERROR: DJANGO_CSRF_TRUSTED_ORIGINS is not set."
  exit 1
fi

echo "[2/5] Django deploy security checks"
DJANGO_DEBUG=False uv run python manage.py check --deploy --fail-level WARNING

echo "[3/5] Migration plan"
DJANGO_DEBUG=False uv run python manage.py migrate --plan

echo "[4/5] Frontend tests"
cd frontend
npm run test

echo "[5/5] Frontend build"
npm run build

echo "Pre-deploy checks passed."
