# MovieLensApp
# Python program that reads/updates MovieLens database in SQLite.
# I used the MovieLens database which contains more than 45,000 movies and approximately 100,000 reviews, to generate an answer depending on user's input. # I developed this app in a python environment, using N-tier design, which is a software design pattern that separates an application into multiple layers or tiers, each with its own specific role. 
# datatier.py provides functions to interact with a database using SQL queries. The module includes three functions: select_one_row, select_n_rows, and perform_action.
# The module uses the SQLite3 library to connect to a database and execute SQL queries. In this case, the datatier.py module acts as the data access layer, which handles all interactions with the database. 
# objecttier builds movie-related objects from data retrieved through a data tier. 
# This app has 5 commands in total. (Working on more)
# 1. lookup movies by name/pattern,
# 2. lookup details about a specific movie,
# 3. top N movies by average rating,
# 4. insert a review, and
# 5. set a movie’s tagline
