FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Installl Chrome and Chromedriver for Selenium
RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb \
    && apt-get update \
    && apt-get install -y ./chrome.deb --no-install-recommends \
    && rm ./chrome.deb \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && LATEST_CHROMEDRIVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE") \
    && echo "Installing chromedriver version: "$LATEST_CHROMEDRIVER \
    && curl -L "https://chromedriver.storage.googleapis.com/${LATEST_CHROMEDRIVER}/chromedriver_linux64.zip" -o chromedriver_linux64.zip \
    && apt-get update \
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

CMD ["python", "/app/src/app.py"]
