This is my first project in Django. I created simple REST API using Django and PostgreSQL database.
There are 3 endpoints: albums, songs, playlists. I prepared GET, POST, PATCH, PUT, and DELETE method for each endpoint.
I implemented also safe delete data from a database, the data is kept after deleting but the column of the date of deletion is filed.
Moreover, I added logs in a middleware to track all SQL queries which are sent to the database and server errors.

I didn't use Django Rest Framework, because in this project I wanted to get know better the core of Django framework.

I disable CSRF only for education needed.
