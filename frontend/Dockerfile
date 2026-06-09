FROM node:26.3.0-trixie-slim AS base
ENV HOST=0.0.0.0
ENV PORT=8080
WORKDIR /app


FROM base AS base2
COPY nuxtapp/package*.json .
RUN npm ci


FROM base2 AS base3
COPY nuxtapp .
RUN npm run build


FROM base2 AS dev
COPY nuxtapp .
CMD ["npm", "run", "dev"]


FROM base AS prod
COPY --from=base3 /app/.output .
RUN useradd -u 12345 -U -s /sbin/nologin app
USER app
CMD ["node", "server/index.mjs"]
