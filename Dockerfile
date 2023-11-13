FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app/src

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev curl build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define a default Chrome and ChromeDriver version
ENV CHROME_VERSION=114.0.5735.198
ENV DEFAULT_CHROMEDRIVER_VERSION=114.0.5735.90

# Install specific Chrome version
RUN curl "http://mirror.cs.uchicago.edu/google-chrome/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_VERSION}-1_amd64.deb" -o chrome.deb \
    && apt-get update \
    && apt-get install -y ./chrome.deb --no-install-recommends \
    && rm ./chrome.deb

# Attempt to get Chrome version and fetch corresponding ChromeDriver
RUN CHROME_INSTALLED_VERSION=$(google-chrome --version | awk '{ print $3 }' | cut -d'.' -f1) \
    && LATEST_CHROMEDRIVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_INSTALLED_VERSION" || echo $DEFAULT_CHROMEDRIVER_VERSION) \
    && echo "Installing chromedriver version: "$LATEST_CHROMEDRIVER \
    && curl -L "https://chromedriver.storage.googleapis.com/${LATEST_CHROMEDRIVER}/chromedriver_linux64.zip" -o chromedriver_linux64.zip \
    && apt-get install -y unzip --no-install-recommends \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/bin/chromedriver \
    && rm chromedriver_linux64.zip \
    && apt-get purge --auto-remove -y unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN pip install --upgrade Flask Werkzeug

COPY src /app/src

CMD ["gunicorn", "-b", "0.0.0.0:8080", "-k", "gevent", "--workers", "4", "src.app:app"]