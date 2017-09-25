# Properties Management System

This python package provides a basic django admin to create users including landlords and tenants, estates and contract. Also provides RESTFul API and a cron job to send notification when contract is about to end

# Installation
```sh
make setup
```

# Run


```sh
make run  # run the server only
make run-all  #setup crontab and run the server 
```

# How to Use
When server is up, browse localhost:8000/admin to play the admin site with credential admin/landlady, or go to localhost:8000 to try the API.

# Testing

```sh
make test
```
