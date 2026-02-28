FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install Flask requests
# Only expose the port for this specific service
EXPOSE 53533/udp
CMD ["python", "authoritative_server.py"]