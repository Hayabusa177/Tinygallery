# Tinygallery
A tiny gallery web application created by flask, 

# Installation Instructions:

Change work direction
```
  cd <path>
```

Create virtual environment
```
  python -m venv venv
```

Switch to virtual environment
```
  source ./venv/bin/activate
```

Install dependencies
```
  pip install -r ./requirements.txt
```
Initialization database
```
  flask --app tinyGallery init-db
```
 
Start WSGI server
```
  waitress-serve --host 127.0.0.1 --call tinyGallery:create_app
```

Proxy WSGI server with http server for example :nginx

* add some config to /etc/nginx/nginx.conf
```
  server {
    listen 17779;
    listen [::]:17779 ipv6only=on;
    server_name tinyGallery;
        
    location / {
        proxy_pass http://127.0.0.1:8080/;
    }
}
```

Start nginx
```
  systemctl start nginx
```
