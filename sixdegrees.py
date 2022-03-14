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
    actor_id = details["results"][0]["id"]
    if actor_id > 999997:
        tryagain = input("That actor is not yet available.  Please try another: ")
        return get_actor_id_from_name(tryagain)
    return str(actor_id)


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
    # given list of actors new to the current iteration,
    # find the list of movies they have been in excluding those already processed,
    # then get the new list of actors from these new movies, excluding those already processed
    # run recursively until the target actor is found or max steps exceeded
    if count >= 5:
        return -1
    new_actor_list = []  # will hold the new actors not included in previous iterations
    # iterate the current list of actors and process
    for actor in actors:
        if actor > 999997:
            continue
        new_movie_list = []  # to hold the new movies not included in previous iterations
        movie_list = get_movie_list(actor)
        # iterate the current actor's list of movies
        for movie in movie_list:
            if movie > 921035:
                continue
            # if the current movie hasn't been processed previously, append to both tree & list
            if not mtree.search(mroot, movie):
                new_movie_list.append(movie)
                mroot = mtree.insert(mroot, movie, actor)

        # iterate new movies and add any new actors for the next iteration. Stop if target is found
        for movie in new_movie_list:
            actor_list = get_cast_list(movie)
            for actr in actor_list:
                if actr > 999997:
                    continue
                if not atree.search(aroot, actr):
                    new_actor_list.append(actr)
                    aroot = atree.insert(aroot, actr, movie)
                if actr == target:
                    path = [actr, movie]
                    path = backtrack(path, atree, mtree, aroot, mroot)
                    return path

    return check_connections(new_actor_list, atree, aroot, mtree, mroot, count + 1, target)


def backtrack(path, atree, mtree, aroot, mroot):
    # trace sources back to build the path
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


def print_results(res, acount, mcount):
    path = res[-2::-1]
    print("Found a path with " + str(len(path) // 2) + " degrees of separation!")
    print(path)

    print(get_actor_name_from_id(path[0]) + " appeared in ", end="")
    for num in range(1, len(path) - 1):
        if num % 2 == 0:
            name = get_actor_name_from_id(path[num])
            print(name + ", who appeared in ", end="")
        else:
            title = get_movie_name_from_id(path[num])
            print(title + " with ", end="")
    print(get_actor_name_from_id(path[-1]))
    print("processed " + str(acount) + " actors and " + str(mcount) + " movies")


def run():
    while True:
        actor_tree = AVL.Tree()
        movie_tree = AVL.Tree()
        actor_root = None
        movie_root = None

        actor1 = input("Enter an actor: ")
        actor1 = int(get_actor_id_from_name(actor1))
        actor2 = input("Enter an actor: ")
        actor2 = int(get_actor_id_from_name(actor2))

        actor_list = [actor1]
        actor_root = actor_tree.insert(actor_root, actor1, None)
        res = check_connections(actor_list, actor_tree, actor_root, movie_tree, movie_root, 0, actor2)
        if res == -1:
            print("Congratulations, you've stumped me!")
            exit()

        print_results(res, actor_tree.num_of_nodes, movie_tree.num_of_nodes)

        cont = input("Enter 0 to exit or any other input to continue")
        if cont == "0":
            exit()


run()
