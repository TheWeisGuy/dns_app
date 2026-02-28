FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install Flask requests
EXPOSE 8080 9090 53533/udp