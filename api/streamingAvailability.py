

import requests
from json import loads as loadJson
from modules.misc import doesCachedFileExist, loadFileFromCache, saveFileToCache

def getStreamingAvailabilityFor(imdbId):
    """ Returns a list of movies.
    Elements for each movie in the dict:

    imdbRating : int --> 88
    Year   : str --> 2019
    imdbID : str --> tt4154796
    Type   : str --> movie
    Poster : str --> https://m.media-amazon.com/images/M/MV5BMTc5MDE2ODcwNV5BMl5BanBnXkFtZTgwMzI2NzQ2NzM@._V1_SX300.jpg
    """

    # Caching stuff
    if doesCachedFileExist('availabilityOf_' + imdbId + '.json'):
        return loadFileFromCache('availabilityOf_' + imdbId + '.json')

    url = "https://streaming-availability.p.rapidapi.com/get/basic"

    querystring = {"country":"at","imdb_id": imdbId, "output_language":"en"}

    headers = {
        "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com",
        "X-RapidAPI-Key": "c49163ae7cmsh07d1242fe9581cfp18f04djsnfe1cde4a1b7a"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 404:
        print("No movie found for imdbId", imdbId)
        return False
    
    result = loadJson(response.text)

    # Caching stuff
    #if config.DEBUG and not doesCachedFileExist('movieInfo.json'):
    saveFileToCache('availabilityOf_' + imdbId + '.json', result)
    return result
