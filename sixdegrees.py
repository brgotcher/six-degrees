import requests
import linecache
import AVL

KEY = "fd1ba63489529c937b3759165608f6cd"



def getActorIDFromName(name):
    # take a string representing an actor's name and send a GET request to tmdb to get their unique ID number
    name = name.replace(" ", "+")
    details = requests.get("https://api.themoviedb.org/3/search/person?api_key=" + KEY + "&query=" + name)
    details = details.json()
    # check for a valid response to the GET request
    if not details["results"]:
        tryagain = input("Error: Actor not found check spelling and try again\nEnter an actor: ")
        return getActorIDFromName(tryagain)
    # pull ID number from results and return
    id = str(details["results"][0]["id"])
    return id


def getMovieList(id):
    # take an actor ID number and return list of movie ID numbers for movies they have appeared in
    # pull corresponding line from actors.txt
    movies = linecache.getline("actors.txt", id)
    # movies is a string, if length less than 4 there won't be any valid ID numbers, so return empty list
    if len(movies) < 4:
        return []
    # break string down into a list and return
    movies = movies[1:-2]
    movies = movies.split(", ")
    for i in range(0, len(movies)):
        movies[i] = int(movies[i])
    return movies


def getCastList(id):
    # take movie ID and return list of actors IDs for actors that appeared in the movie
    cast = linecache.getline("movies.txt", id)
    length = len(cast)
    if length < 4:
        return []
    cast = cast[1:-2]
    cast = cast.split(", ")
    for i in range(0, len(cast)):
        cast[i] = int(cast[i])
    return cast


def getMovieNameFromID(id):
    # take movie ID number, send get request to tmdb to retrieve the movie's name
    data = requests.get("https://api.themoviedb.org/3/movie/" + str(id) + "?api_key=" + KEY)
    data = data.json()
    title = data["title"]
    return title


def getActorNameFromID(id):
    # take actor ID number, send get request to tmdb to retrieve the actor's name
    data = requests.get("https://api.themoviedb.org/3/person/" + str(id) + "?api_key=" + KEY)
    data = data.json()
    name = data["name"]
    return name


def checkConnections(actors, aTree, aRoot, mTree, mRoot, count, target):
    #
    if count >= 5:
        return -1
    newActorList = []
    for actor in actors:
        if actor > 999997:
            continue
        newMovieList = []
        movieList = getMovieList(actor)
        for movie in movieList:
            if movie > 921035:
                continue
            # if movie not in movies and movie not in newMovieList:
            if not mTree.search(mRoot, movie):
                newMovieList.append(movie)
                mRoot = mTree.insert(mRoot, movie, actor)
        for movie in newMovieList:
            actorList = getCastList(movie)
            for actr in actorList:
                if actr > 999997:
                    continue
                # if actr not in actors and actr not in newActorList:
                if not aTree.search(aRoot, actr):
                    newActorList.append(actr)
                    aRoot = aTree.insert(aRoot, actr, movie)
                if actr == target:
                    path = [actr, movie]
                    path = backtrack(path, aTree, mTree, aRoot, mRoot)
                    return path

    return checkConnections(newActorList, aTree, aRoot, mTree, mRoot, count+1, target)


def backtrack(path, aTree, mTree, aRoot, mRoot):
    pathlength = len(path)
    last = path[pathlength-1]
    if last == None:
        return path
    if pathlength % 2 == 0:
        path.append(mTree.search(mRoot, last).src)
        return backtrack(path, aTree, mTree, aRoot, mRoot)
    else:
        path.append(aTree.search(aRoot, last).src)
        return backtrack(path, aTree, mTree, aRoot, mRoot)


while True:
    actorTree = AVL.Tree()
    movieTree = AVL.Tree()
    actorRoot = None
    movieRoot = None

    actor1 = input("Enter an actor: ")
    actor1 = int(getActorIDFromName(actor1))
    while actor1 > 999997:
        actor1 = input("That actor is not yet available.  Please try another: ")
        actor1 = int(getActorIDFromName(actor1))
    actor2 = input("Enter an actor: ")
    actor2 = int(getActorIDFromName(actor2))
    while actor2 > 999997:
        actor2 = input("That actor is not yet available.  Please try another: ")
        actor2 = int(getActorIDFromName(actor2))

    actorList = [actor1]
    actorRoot = actorTree.insert(actorRoot, actor1, None)
    res = checkConnections(actorList, actorTree, actorRoot, movieTree, movieRoot, 0, actor2)
    print(res)

    path = res[-2::-1]
    print(path)

    print(getActorNameFromID(actor1) + " appeared in ", end="")
    for i in range(1, len(path)-1):
        if i % 2 == 0:
            name = getActorNameFromID(path[i])
            print(name + ", who appeared in ", end="")
        else:
            title = getMovieNameFromID(path[i])
            print(title + " with ", end="")
    print(getActorNameFromID(actor2))
    cont = input("Enter 0 to exit or any other input to continue")
    if cont == "0":
        exit()
