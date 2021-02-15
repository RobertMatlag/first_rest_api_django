This is my first project in django. I create simple rest api using Django and postgreSQL database.
There are 3 endpoints: albums, songs, playlists. I prepared GET, POST, PATCH, PUT, and DELETE method for each endpoint.
I implemented also safe delte data from database, the data are kept after deleting but column with datatime of deleting is filling.
Moreover I added logs in middleware to track all SQL queries which are sent to database and errors.

I didn't use DRF, because it is project to get know better core of django. 

I disable CSRF only for education needed.
