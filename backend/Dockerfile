FROM python:3.14.2-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1



FROM base AS builder

COPY . .
RUN pip install --no-cache-dir -r requirements.txt



FROM builder AS tester

ARG TEST_MODE=strict
ENV SQLALCHEMY_DATABASE_URI=sqlite:///:memory:
ENV JWT_SECRET_KEY=test-secret

RUN case "$TEST_MODE" in \
        "none") echo "skipped" > app-test-log.txt ;; \
        "lax") pytest src/flaskapi/tests > app-test-log.txt 2>&1 || true ;; \
        "strict") pytest src/flaskapi/tests && echo "success" > app-test-log.txt;; \
    esac
RUN rm -r src/flaskapi/tests && pip uninstall -y pytest



FROM base AS runner

WORKDIR /src

RUN groupadd -g 1000 app && useradd -u 1000 -g app -s /sbin/nologin app

COPY --from=tester /usr/local /usr/local
COPY --from=tester --chown=app:app /src .
COPY --from=tester /app-test-log.txt /var/log

USER app

CMD ["sh", "cmd.sh"]
