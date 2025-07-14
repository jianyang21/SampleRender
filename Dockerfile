FROM python:3.10-slim

# Install Chrome dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg unzip xvfb \
    libxi6 libgconf-2-4 libappindicator1 libindicator7 \
    libnss3 libxss1 libasound2 libxshmfence1 libgbm-dev libgtk-3-0

# Install Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome*.deb || apt-get -fy install

# Install ChromeDriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` \
    && wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip \
    && unzip chromedriver_linux64.zip \
    && mv chromedriver /usr/local/bin/ \
    && chmod +x /usr/local/bin/chromedriver

# Set display port for Xvfb
ENV DISPLAY=:99

# Set working directory
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Start script
CMD ["xvfb-run", "--auto-servernum", "--server-args='-screen 0 1024x768x24'", "python", "scraper.py"]
