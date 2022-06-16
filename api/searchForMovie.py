
import requests
from json import loads as loadJson
from modules.misc import doesCachedFileExist, loadFileFromCache, saveFileToCache

def getMovieInfoFor(searchString):
    """ Returns a list including multiple movies related to the search string.
    Elements for each movie in the dict:

    Title  : str --> Avengers: Endgame
    Year   : str --> 2019
    imdbID : str --> tt4154796
    Type   : str --> movie
    Poster : str --> https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_SX300.jpg
    """

    if doesCachedFileExist('movieInfoFor_' + searchString + '.json'):
        return loadFileFromCache('movieInfoFor_' + searchString + '.json')

    print("[API] SearchMovieInfo Call for", searchString)

    url = "https://movie-database-alternative.p.rapidapi.com/"
    querystring = {
        "s" : str(searchString),
        "r" : "json",
        "page" : "1"
    }

    headers = {
        "X-RapidAPI-Host": "movie-database-alternative.p.rapidapi.com",
        "X-RapidAPI-Key": "yourAPIkey"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = loadJson(response.text)
    if response['Response'] == 'True':
        result = response['Search']
        result = [entry for entry in result if entry['Type'] == 'movie']
    else:
        return False # Movie not found

    saveFileToCache('movieInfoFor_' + searchString + '.json', result)
    return result