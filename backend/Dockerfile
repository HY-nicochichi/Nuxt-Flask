FROM python:3.14.2-slim-trixie AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV APP_RUN_MODE=production
ENV APP_CONCURRENCY=20

WORKDIR /src



FROM base AS builder

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -f requirements.txt

COPY cmd.sh .
COPY flaskapi .
COPY swagger.yaml .



FROM builder AS tester

ARG TEST_MODE=strict
ENV PYTEST_ADDOPTS="-p no:cacheprovider"
ENV APP_RUN_MODE=test

RUN case "$TEST_MODE" in \
        "none") echo "skipped" > /app-test-log.txt ;; \
        "lax") pytest tests > /app-test-log.txt 2>&1 || true ;; \
        "strict") pytest tests && echo "success" > /app-test-log.txt;; \
    esac
RUN rm -rf tests && pip uninstall -y pytest



FROM base AS runner

RUN groupadd -g 1000 app && \
    useradd -u 1000 -g app -s /sbin/nologin app

COPY --from=tester /usr/local /usr/local
COPY --from=tester /src .
COPY --from=tester /app-test-log.txt /var/log

USER app

CMD ["sh", "cmd.sh"]
