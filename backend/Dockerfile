FROM python:3.13-slim

# Set the working directory
WORKDIR /app

# Copy the necessary files
COPY pyproject.toml poetry.lock ./

# Copy the rest of the application code
COPY . .

RUN pip install poetry && poetry install --only main

# Install PyTesseract
RUN apt-get update && apt-get install -y tesseract-ocr libtesseract-dev poppler-utils

# Run the application
CMD ["poetry", "run", "start"]