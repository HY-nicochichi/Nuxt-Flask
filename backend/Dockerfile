FROM python:3.14.5-slim-trixie AS base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
ENV APP_CONCURRENCY=10
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt
CMD ["gunicorn"]


FROM base AS base2
COPY gunicorn.conf.py .
COPY swagger.yaml .
COPY src ./src


FROM base AS dev
ENV PYTEST_ADDOPTS="-p no:cacheprovider"
RUN apt update -qq && \
    apt install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache pytest==9.0.3 pyright==1.1.411
COPY --from=base2 /app .
COPY tests ./tests


FROM base2 AS prod
RUN useradd -u 12345 -U -s /sbin/nologin app
USER app
