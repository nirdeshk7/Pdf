FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libreoffice \
    ghostscript \
    curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app.py ./app.py
COPY frontend/templates/ ./templates/

RUN mkdir -p uploads converted_pdfs temp_outputs

EXPOSE 5000
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
