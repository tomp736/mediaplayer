FROM python:3.7-alpine

RUN adduser -D worker
RUN apk add  --no-cache ffmpeg

# Create a working directory and copy the application code into it
WORKDIR /app
USER worker
ENV PATH="/home/worker/.local/bin:${PATH}"


COPY ./src/requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY ./src .

# Set environment variables for the Flask application
# ENV PYTHONHASHSEED= set to have consistant hashes
ENV FLASK_APP=app.py
ENV FLASK_DEBUG=False
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=80

# Run the application
CMD ["python", "app.py"]