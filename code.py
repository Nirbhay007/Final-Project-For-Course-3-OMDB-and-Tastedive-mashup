import requests_with_caching
import sys
sys.setExecutionLimit(100000)

def get_movies_from_tastedive(name):

    url = 'https://tastedive.com/api/similar'

    pm = {'q':name,'type':'movies','limit':5}

    res = requests_with_caching.get(url, params=pm)

    js = res.json()

    return js

def extract_movie_titles(js):

    lst = [d['Name'] for d in js['Similar']['Results']]

    return lst

def get_related_titles(movies):

    movie_list = list()

    for movie in movies:

        for i in extract_movie_titles(get_movies_from_tastedive(movie)):

            movie_list.append(i)

    return list(set(movie_list))

def get_movie_data(mov):

    par = {'t':mov ,'r':'json'}

    url = 'http://www.omdbapi.com/'

    res = requests_with_caching.get(url,params=par).json()

    return res
def get_movie_rating(movieNameJson):
    strRanting=""
    for typeRantingList in movieNameJson["Ratings"]:
        if typeRantingList["Source"]== "Rotten Tomatoes":
            strRanting = typeRantingList["Value"]
    if strRanting != "":
        ranting = int(strRanting[:2])
    else: ranting = 0
    return ranting

def get_sorted_recommendations(listMovieTitle):
    listMovie= get_related_titles(listMovieTitle)
    listMovie= sorted(listMovie, key = lambda movieName: (get_movie_rating(get_movie_data(movieName)), movieName), reverse=True)
    
    return listMovie

print(get_sorted_recommendations(["Bridesmaids", "Sherlock Holmes"]))
