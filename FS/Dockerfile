FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install Flask requests
# Expose the TCP port for Fibonacci calculations
EXPOSE 9090
CMD ["python", "fibonacci_server.py"]