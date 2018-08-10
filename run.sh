cd /var/www/disqus2lean/
gunicorn --workers=2 main:app -b 0.0.0.0:8080
