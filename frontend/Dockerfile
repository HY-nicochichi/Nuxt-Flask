FROM node:26.3.0-trixie-slim AS builder

COPY . .
WORKDIR /nuxtapp

RUN npm install
RUN npm run build



FROM builder AS tester

ARG TEST_MODE=strict
ENV API_URL_BASE=/test-api
ENV FORCE_SSL_COOKIE=1

RUN case "$TEST_MODE" in \
        "none") echo "skipped" > /app-test-log.txt ;; \
        "lax") npm run test > /app-test-log.txt 2>&1 || true ;; \
        "strict") npm run test && echo "success" > /app-test-log.txt ;; \
    esac



FROM node:26.3.0-trixie-slim AS runner

ENV NITRO_HOST=0.0.0.0
ENV NITRO_PORT=8080

WORKDIR /src

RUN useradd -u 12345 -U -s /sbin/nologin -m app

COPY --from=tester /nuxtapp/.output .
COPY --from=tester /app-test-log.txt /var/log

USER app

CMD ["node", "server/index.mjs"]
