FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --home-dir /app app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=app:app . .

RUN mkdir -p /data /app/staticfiles \
    && chown -R app:app /data /app/staticfiles

USER app

EXPOSE 8000

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "60"]
