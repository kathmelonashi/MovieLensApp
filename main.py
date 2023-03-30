# Kathleen Melonashi
# UIN: 674867629, NetID: kmelo2
# Project 2: MovieLens Application
# CS341: Programming Language Concepts
# Spring 2023

import sqlite3
import objecttier

##############################################################################


def general_stats(db):
  # General stats function - Gets and prints out the number of movies and reviews in the database.
  print("General stats:")
  numMov = objecttier.num_movies(dbConn)
  numRev = objecttier.num_reviews(dbConn)
  print("  # of movies:", f"{numMov:,}")
  print("  # of reviews:", f"{numRev:,}")
  print()


##############################################################################


def command1(db):
  # command1 function - Takes as input movie name and return the number of movies with that title are found in the database.
  movName = input("Enter movie name (wildcards _ and % supported): ")
  print()

  getMov = objecttier.get_movies(dbConn, movName)

  if getMov is None:
    print("# of movies found: 0")
  elif len(getMov) > 100:
    print("# of movies found:", (len(getMov)))
    print()
    print(
      "There are too many movies to display, please narrow your search and try again..."
    )
  else:
    print("# of movies found:", (len(getMov)))
    print()

    for m in getMov:
      print(m.Movie_ID, ":", m.Title, f"({m.Release_Year})")


##############################################################################


def command2(db):
  # commnand2 function - Takes as input a movie id and returns all the details of that movie using out function get_movie_details from objecttier.

  MovID = input("Enter movie id: ")
  print()

  getMovDet = objecttier.get_movie_details(dbConn, MovID)

  if getMovDet is None:
    print("No such movie...")
  else:
    print(getMovDet.Movie_ID, ":", getMovDet.Title)
    print("  Release date:", getMovDet.Release_Date)
    print("  Runtime:", getMovDet.Runtime, "(mins)")
    print("  Orig language:", getMovDet.Original_Language)
    print("  Budget:", f"${getMovDet.Budget:,}", "(USD)")
    print("  Revenue:", f"${getMovDet.Revenue:,}", "(USD)")
    print("  Num reviews:", getMovDet.Num_Reviews)
    print("  Avg rating:", f"{getMovDet.Avg_Rating:.2f}", "(0..10)")
    print("  Genres: ", end="")

    # For loop to get the list of genres and print them out.
    for p in getMovDet.Genres:
      print(p + ", ", end="")
    print()
    # For loop to get the list of companies and print them out.
    print("  Production companies: ", end="")
    for p in getMovDet.Production_Companies:
      print(p + ", ", end="")
    print()
    print("  Tagline: " + str(getMovDet.Tagline))


##############################################################################


def command3(db):
  # command3 function - gets number of movies and ratings as input and returns the top N movies using function get_top_N_movies from objecttier.
  n = int(input("N? "))
  # Error check for N and min number of reviews before we proceed.
  if n <= 0:
    print("Please enter a positive value for N...")
    print()
    return
  rev = int(input("min number of reviews? "))
  if rev <= 0:
    print("Please enter a positive value for min number of reviews...")
    print()
    return
  print()

  topN = objecttier.get_top_N_movies(dbConn, n, rev)

  if topN is None:
    return
  else:
    for n in topN:
      print(n.Movie_ID, ":", n.Title, f"({n.Release_Year}),", "avg rating =",
            f"{n.Avg_Rating:.2f}", f"({n.Num_Reviews} reviews)")


##############################################################################


def command4(db):
  # command4 function - User inputs ratings from 1 to 10 for one perticular movie id.
  rating = int(input("Enter rating (0..10): "))

  if rating < 0 or rating > 10:
    print("Invalid rating...")
    return
  else:
    movID = int(input("Enter movie id: "))
    getMov = objecttier.add_review(dbConn, movID, rating)
    print()
    if getMov == 0:
      print("No such movie...")
    else:
      print("Review successfully inserted")


##############################################################################
def command5(db):

  tag = input("tagline? ")
  movID = int(input("movie id? "))
  
  getMov = objecttier.set_tagline(dbConn, movID, tag)
  print()
  if getMov == 0:
    print("No such movie...")
  else:
    print("Tagline successfully set")

###############################################################################
# main
#
##############################################################################

dbConn = sqlite3.connect('MovieLens.db')

print('** Welcome to the MovieLens app **')
print()

general_stats(dbConn)

cmd = input("Please enter a command (1-5, x to exit): ")
print()

while cmd != "x":
  if cmd == "1":
    command1(dbConn)
  elif cmd == "2":
    command2(dbConn)
  elif cmd == "3":
    command3(dbConn)
  elif cmd == "4":
    command4(dbConn)
  elif cmd == "5":
    command5(dbConn)
  else:
    print("**Error, unknown command, try again...")

  print()
  cmd = input("Please enter a command (1-5, x to exit): ")
  print()

dbConn.close()
#
# done
#
