#
# objecttier
#
# Builds Movie-related objects from data retrieved through
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#

import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:

  def __init__(self, id, title, release_year):
    self._Movie_ID = int(id)
    self._Title = str(title)
    self._Release_Year = str(release_year)

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year


##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:

  def __init__(self, id, title, release_year, num_reviews, avg_rating):
    self._Movie_ID = int(id)
    self._Title = str(title)
    self._Release_Year = str(release_year)
    self._Num_Reviews = int(num_reviews)
    self._Avg_Rating = float(avg_rating)

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year

  @property
  def Avg_Rating(self):
    return self._Avg_Rating

  @property
  def Num_Reviews(self):
    return self._Num_Reviews


##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:

  def __init__(self,
               id,
               title,
               release_date,
               runtime,
               langauge,
               budget,
               revenue,
               num_reviews,
               avg_rating,
               tagline,
               genres=[],
               production_companies=[]):
    self._Movie_ID = int(id)
    self._Title = str(title)
    self._Release_Date = str(release_date)
    self._Runtime = int(runtime)
    self._Original_Language = str(langauge)
    self._Budget = int(budget)
    self._Revenue = int(revenue)
    self._Num_Reviews = int(num_reviews)
    self._Avg_Rating = float(avg_rating)
    self._Tagline = str(tagline)
    self._Genres = genres
    self._Production_Companies = production_companies

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Date(self):
    return self._Release_Date

  @property
  def Runtime(self):
    return self._Runtime

  @property
  def Original_Language(self):
    return self._Original_Language

  @property
  def Budget(self):
    return self._Budget

  @property
  def Revenue(self):
    return self._Revenue

  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Rating

  @property
  def Tagline(self):
    return self._Tagline

  @property
  def Genres(self):
    return self._Genres

  @property
  def Production_Companies(self):
    return self._Production_Companies


##################################################################
#
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
  # Query to get number of movies
  sql = "select count(movie_ID) from Movies"

  row = datatier.select_one_row(dbConn, sql)

  # handle error
  if row is None:
    return -1
  elif row == ():
    return -1

  for r in row:
    return r

  return -1


##################################################################
#
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
  # Query to get number of reviews
  sql = "Select count(Rating) From Ratings;"

  row = datatier.select_one_row(dbConn, sql)

  # handle error
  if row is None:
    return -1

  for r in row:
    return r

  return -1


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name;
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
  sql = """Select movie_ID, title, strftime('%Y',Release_Date)
 From Movies
 Where title like ?
 Order by movie_id asc;"""

  rows = datatier.select_n_rows(dbConn, sql, [pattern])
  getMovies = []

  if rows is None:
    return []
  else:
    for row in rows:
      movie = Movie(row[0], row[1], row[2])
      getMovies.append(movie)
  return getMovies


##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
  # Query that creates table containing movie ID, title, date, runtime, language, budget, revenue, num of reviews, average of rating and taglines. Joining Ratings and Movie_taglines
  sql = "Select Movies.Movie_ID, Movies.Title, \
  date(Release_Date), Runtime, Original_Language, \
  Budget, Revenue, count(Ratings.Rating),avg(Ratings.rating),\
  Movie_Taglines.Tagline \
  From Movies Left Join Movie_Taglines \
  On Movies.Movie_ID = Movie_Taglines.Movie_ID \
  Left Join Ratings \
  On Ratings.Movie_ID = Movies.Movie_ID \
  Where Movies.Movie_ID like ?; "

  row_movie = datatier.select_one_row(dbConn, sql, [movie_id])

  # handle error
  if row_movie[0] == None:
    return None

  # Query that creates table with all the genres of the movie since there is more than one for each movie ID.
  sql2 = "Select Genres.Genre_Name \
  From Genres Join Movie_Genres \
  On Genres.Genre_ID = Movie_Genres.Genre_ID \
  Where Movie_Genres.Movie_ID like ? \
  Order by Genres.Genre_Name asc;"

  row_genre = datatier.select_n_rows(dbConn, sql2, [movie_id])

  # Store all genres of a movie in a list.
  allGenres = []
  for r in row_genre:
    allGenres.append(r[0])

  # Query that creates table with all the production company names of a movie id.
  sql3 = "Select Companies.Company_Name \
  From Companies Join Movie_Production_Companies \
  On Companies.Company_ID = Movie_Production_Companies.Company_ID \
  Where Movie_Production_Companies.Movie_ID like ? \
  Order by Companies.Company_name asc;"

  row_companies = datatier.select_n_rows(dbConn, sql3, [movie_id])

  # Store all production companies of a movie in a list.
  allCompanies = []
  for r in row_companies:
    allCompanies.append(r[0])

  ## handle the diffrent possible cases of tagline, and avg_rating
  if (row_movie[8] == None):
    avg_rating = float(0.00)
  else:
    avg_rating = row_movie[8]

  if (row_movie[9] == None):
    tagline = ""
  else:
    tagline = row_movie[9]

  movie_details = MovieDetails(row_movie[0], row_movie[1], row_movie[2],
                               row_movie[3], row_movie[4], row_movie[5],
                               row_movie[6], row_movie[7], avg_rating, tagline,
                               allGenres, allCompanies)

  return movie_details


##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
  # Query to get the top movies with the users input.
  sql = """ Select Movies.Movie_ID , title, strftime('%Y',Release_Date),  avg(Ratings.rating),count(Ratings.rating) \
  From Movies Join Ratings \
  On (Ratings.Movie_ID = Movies.Movie_ID) \
  Group by Movies.Movie_ID \
  Having count(Ratings.Rating) >= ?  \
  Order by avg(Ratings.Rating) desc \
  limit ?  """

  rows = datatier.select_n_rows(dbConn, sql, [min_num_reviews, N])
  if rows == None:
    return []
  elif rows == []:
    return []

  gettopNMovies = []
  for x in rows:
    movie_rating = MovieRating(x[0], x[1], x[2], x[4], x[3])
    gettopNMovies.append(movie_rating)

  return gettopNMovies


##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):

  sql = "Insert Into Ratings(Movie_ID, Rating) Values (?,?);"
  sql2 = "Select Movie_ID From Movies Where Movie_ID = ?"

  row = datatier.select_one_row(dbConn, sql2, [movie_id])

  if row is None or row == ():
    return 0
  if rating > 10 or rating < 0:
    return 0

  p = datatier.perform_action(dbConn, sql, [movie_id, rating])
  return p


##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):

  sql = "Select Movie_Id From Movies Where Movie_Id = ?"

  movie = datatier.select_one_row(dbConn, sql, [movie_id])
  if movie is None or movie == (): 
    return 0

  update = "UPDATE Movie_Taglines SET Tagline = ? WHERE Movie_Id = ?;"

  tag = "Select Tagline from Movie_Taglines Where Movie_Id = ?"

  tag2 = "INSERT INTO Movie_Taglines (Movie_Id, Tagline) VALUES (?, ?);"

  tagC = datatier.select_one_row(dbConn, tag, [movie_id])

  if tagC is None or tagC == ():
    p = datatier.perform_action(dbConn, tag2, [movie_id, tagline])
  else:
    p = datatier.perform_action(dbConn, update, [tagline, movie_id])
    
  return p
