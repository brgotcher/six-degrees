import requests
import linecache
import AVL

KEY = "fd1ba63489529c937b3759165608f6cd"


def get_actor_id_from_name(actor_name):
    # take a string representing an actor's name and send a GET request to tmdb to get their unique ID number
    actor_name = actor_name.replace(" ", "+")
    details = requests.get("https://api.themoviedb.org/3/search/person?api_key=" + KEY + "&query=" + actor_name)
    details = details.json()
    # check for a valid response to the GET request
    if not details["results"]:
        tryagain = input("Error: Actor not found check spelling and try again\nEnter an actor: ")
        return get_actor_id_from_name(tryagain)
    # pull ID number from results and return
    actor_id = str(details["results"][0]["id"])
    return actor_id


def get_movie_list(actor_id):
    # take an actor ID number and return list of movie ID numbers for movies they have appeared in
    # pull corresponding line from actors.txt
    movies = linecache.getline("actors.txt", actor_id)
    # movies is a string, if length less than 4 there won't be any valid ID numbers, so return empty list
    if len(movies) < 4:
        return []
    # break string down into a list and return
    movies = movies[1:-2]
    movies = movies.split(", ")
    for i in range(0, len(movies)):
        movies[i] = int(movies[i])
    return movies


def get_cast_list(movie_id):
    # take movie ID and return list of actors IDs for actors that appeared in the movie
    cast = linecache.getline("movies.txt", movie_id)
    length = len(cast)
    if length < 4:
        return []
    cast = cast[1:-2]
    cast = cast.split(", ")
    for i in range(0, len(cast)):
        cast[i] = int(cast[i])
    return cast


def get_movie_name_from_id(movie_id):
    # take movie ID number, send get request to tmdb to retrieve the movie's name
    data = requests.get("https://api.themoviedb.org/3/movie/" + str(movie_id) + "?api_key=" + KEY)
    data = data.json()
    return data["title"]


def get_actor_name_from_id(actor_id):
    # take actor ID number, send get request to tmdb to retrieve the actor's name
    data = requests.get("https://api.themoviedb.org/3/person/" + str(actor_id) + "?api_key=" + KEY)
    data = data.json()
    return data["name"]


def check_connections(actors, atree, aroot, mtree, mroot, count, target):
    #
    if count >= 5:
        return -1
    new_actor_list = []
    for actor in actors:
        if actor > 999997:
            continue
        new_movie_list = []
        movie_list = get_movie_list(actor)
        for movie in movie_list:
            if movie > 921035:
                continue
            # if movie not in movies and movie not in new_movie_list:
            if not mtree.search(mroot, movie):
                new_movie_list.append(movie)
                mroot = mtree.insert(mroot, movie, actor)
        for movie in new_movie_list:
            actor_list = get_cast_list(movie)
            for actr in actor_list:
                if actr > 999997:
                    continue
                # if actr not in actors and actr not in new_actor_list:
                if not atree.search(aroot, actr):
                    new_actor_list.append(actr)
                    aroot = atree.insert(aroot, actr, movie)
                if actr == target:
                    path = [actr, movie]
                    path = backtrack(path, atree, mtree, aroot, mroot)
                    return path

    return check_connections(new_actor_list, atree, aroot, mtree, mroot, count + 1, target)


def backtrack(path, atree, mtree, aroot, mroot):
    path_length = len(path)
    last = path[path_length-1]
    if not last:
        return path
    if path_length % 2 == 0:
        path.append(mtree.search(mroot, last).src)
        return backtrack(path, atree, mtree, aroot, mroot)
    else:
        path.append(atree.search(aroot, last).src)
        return backtrack(path, atree, mtree, aroot, mroot)


while True:
    actorTree = AVL.Tree()
    movieTree = AVL.Tree()
    actorRoot = None
    movieRoot = None

    actor1 = input("Enter an actor: ")
    actor1 = int(get_actor_id_from_name(actor1))
    while actor1 > 999997:
        actor1 = input("That actor is not yet available.  Please try another: ")
        actor1 = int(get_actor_id_from_name(actor1))
    actor2 = input("Enter an actor: ")
    actor2 = int(get_actor_id_from_name(actor2))
    while actor2 > 999997:
        actor2 = input("That actor is not yet available.  Please try another: ")
        actor2 = int(get_actor_id_from_name(actor2))

    actorList = [actor1]
    actorRoot = actorTree.insert(actorRoot, actor1, None)
    res = check_connections(actorList, actorTree, actorRoot, movieTree, movieRoot, 0, actor2)
    # print(res)

    path = res[-2::-1]
    print(path)
    print("Found a path with " + str(len(path)//2) + " Degrees of separation: ")

    print(get_actor_name_from_id(actor1) + " appeared in ", end="")
    for num in range(1, len(path) - 1):
        if num % 2 == 0:
            name = get_actor_name_from_id(path[num])
            print(name + ", who appeared in ", end="")
        else:
            title = get_movie_name_from_id(path[num])
            print(title + " with ", end="")
    print(get_actor_name_from_id(actor2))
    cont = input("Enter 0 to exit or any other input to continue")
    if cont == "0":
        exit()
