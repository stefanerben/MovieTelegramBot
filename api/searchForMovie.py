
import requests
from json import loads as loadJson

def getMovieInfoFor(searchString):
    """ Returns a dictionary including multiple movies related to the search string.
    Elements for each movie in the dict:

    Title  : str --> Avengers: Endgame
    Year   : str --> 2019
    imdbID : str --> tt4154796
    Type   : str --> movie
    Poster : str --> https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_SX300.jpg
    """

    url = "https://movie-database-alternative.p.rapidapi.com/"
    querystring = {
        "s" : str(searchString),
        "r" : "json",
        "page" : "1"
    }

    headers = {
        "X-RapidAPI-Host": "movie-database-alternative.p.rapidapi.com",
        "X-RapidAPI-Key": "c49163ae7cmsh07d1242fe9581cfp18f04djsnfe1cde4a1b7a"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    formatted = loadJson(response.text)

    return formatted['Search']