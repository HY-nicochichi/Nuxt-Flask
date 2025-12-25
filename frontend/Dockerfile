FROM node:25.2.1-slim AS builder

COPY . .
WORKDIR /nuxtapp

RUN npm install
RUN npm run generate



FROM builder AS tester

ARG TEST_MODE=strict

RUN case "$TEST_MODE" in \
        "none") echo "skipped" > /nuxt-test-log.txt ;; \
        "lax") npm run test > /nuxt-test-log.txt 2>&1 || true ;; \
        "strict") npm run test && echo "success" > /nuxt-test-log.txt;; \
    esac



FROM nginx:1.29.4-alpine AS runner

COPY --from=tester /default.conf /etc/nginx/conf.d
COPY --from=tester /nuxtapp/.output/public /usr/share/nginx/html
COPY --from=tester /nuxt-test-log.txt /var/log

CMD ["nginx", "-g", "daemon off;"]
