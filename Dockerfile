# Use Alpine-based Python image
FROM python:3.9-alpine

# Install Apache and necessary modules
RUN apk update && \
    apk add --no-cache apache2 apache2-utils apache2-proxy apache2-http2

# Install mod_proxy to enable reverse proxying
RUN apk add --no-cache apache2-proxy

# Set the working directory in the container
WORKDIR /app

# Copy application requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Configure Apache to reverse proxy requests to the Flask application
RUN echo "ServerName localhost" >> /etc/apache2/httpd.conf && \
    echo "LoadModule proxy_module modules/mod_proxy.so" >> /etc/apache2/httpd.conf && \
    echo "LoadModule proxy_http_module modules/mod_proxy_http.so" >> /etc/apache2/httpd.conf && \
    echo "<VirtualHost *:80>" >> /etc/apache2/httpd.conf && \
    echo "    ProxyPreserveHost On" >> /etc/apache2/httpd.conf && \
    echo "    ProxyPass / http://127.0.0.1:5001/" >> /etc/apache2/httpd.conf && \
    echo "    ProxyPassReverse / http://127.0.0.1:5001/" >> /etc/apache2/httpd.conf && \
    echo "</VirtualHost>" >> /etc/apache2/httpd.conf

# Expose port 80 for Apache
EXPOSE 80

# Set environment variable for Flask app
ENV FLASK_APP=app.py

# Start Flask and Apache in the background
CMD ["sh", "-c", "flask run --host=0.0.0.0 --port=5001 & httpd -D FOREGROUND"]
