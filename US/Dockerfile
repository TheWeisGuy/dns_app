FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install Flask requests
# Expose the TCP port for user interaction
EXPOSE 8080
CMD ["python", "user_server.py"]