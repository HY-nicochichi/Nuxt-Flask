FROM python:3.14.2-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1



FROM base AS builder

COPY . .
RUN pip install -r requirements.txt



FROM builder AS tester

ARG TEST_MODE=strict
ENV SQLALCHEMY_DATABASE_URI=sqlite:///:memory:
ENV JWT_SECRET_KEY=test-secret

RUN case "$TEST_MODE" in \
        "none") echo "skipped" > flask-test-log.txt ;; \
        "lax") pytest src/flaskapi/tests > flask-test-log.txt 2>&1 || true ;; \
        "strict") pytest src/flaskapi/tests && echo "success" > flask-test-log.txt;; \
    esac
RUN rm -r src/flaskapi/tests && pip uninstall -y pytest



FROM base AS runner

WORKDIR /src

COPY --from=tester /usr/local /usr/local
COPY --from=tester /src .
COPY --from=tester /flask-test-log.txt /var/log

CMD ["sh", "cmd.sh"]
