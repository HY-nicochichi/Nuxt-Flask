FROM node:25.4.0-trixie-slim AS builder

ARG API_URL_BASE
ENV API_URL_BASE=${API_URL_BASE}

COPY . .
WORKDIR /nuxtapp

RUN npm install
RUN npm run generate



FROM builder AS tester

ARG TEST_MODE=strict

RUN case "$TEST_MODE" in \
        "none") echo "skipped" > /app-test-log.txt ;; \
        "lax") npm run test > /app-test-log.txt 2>&1 || true ;; \
        "strict") npm run test && echo "success" > /app-test-log.txt;; \
    esac



FROM nginx:1.29.4-alpine3.23-slim AS runner

RUN addgroup -g 1000 app && \
    adduser -D -u 1000 -G app -s /sbin/nologin app

COPY --from=tester /nginx.conf /etc/nginx
COPY --from=tester /nuxtapp/.output/public /usr/share/nginx/html
COPY --from=tester /app-test-log.txt /var/log

USER app

CMD ["nginx", "-g", "daemon off;"]
