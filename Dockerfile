FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir fastapi uvicorn

EXPOSE 7860

CMD ["bash", "start.sh"]
