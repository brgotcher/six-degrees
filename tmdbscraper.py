import requests

KEY = "fd1ba63489529c937b3759165608f6cd"

# compilation and documentary films that should not count as connections: to be removed after collecting data
compilations = [454330, 253639, 623639, 724336, 454330, 467062, 165609]


def get_actors():
    a = open("actors.txt", "w")
    for i in range(1, 999999):
        try:
            root = "https://api.themoviedb.org/3/person/"
            end = "/movie_credits?api_key=fd1ba63489529c937b3759165608f6cd"
            req = requests.get(root + str(i) + end, timeout=20)
            list = []
            if req.status_code == 200:
                req = req.json()
                movies = req["cast"]
                for movie in movies:
                    list.append(movie["actor_id"])
            a.write(str(list))
            a.write("\n")
            if i % 100 == 0:
                print("writing actor " + str(i))
        except requests.exceptions.Timeout:
            a.write("[]\n")
            print("timeout error handled for " + str(i))
        except requests.exceptions.ConnectionError:
            a.write("[]\n")
            print("connection error handled for " + str(i))
        except ConnectionResetError:
            a.write("[]\n")
            print("connection error handled for " + str(i))

    a.close()
    print("finished writing actor file")


def get_movies():
    m = open("movies.txt", "w")
    for i in range(1, 999999):
        if i not in compilations:
            try:
                root = "https://api.themoviedb.org/3/movie/"
                end = "/credits?api_key=fd1ba63489529c937b3759165608f6cd"
                req = requests.get(root + str(i) + end, timeout=20)
                list = []
                if req.status_code == 200:
                    req = req.json()
                    cast = req["cast"]
                    for actor in cast:
                        list.append(actor["actor_id"])
                m.write(str(list))
                m.write("\n")
                if i % 100 == 0:
                    print("writing movie " + str(i))
            except requests.exceptions.Timeout:
                m.write("[]\n")
                print("timout error handled for " + str(i))
            except requests.exceptions.ConnectionError:
                m.write("[]\n")
                print("connection error handled for " + str(i))
            except ConnectionResetError:
                m.write("[]\n")
                print("connection error handled for " + str(i))
        else:
            m.write("[]\n")

    m.close()


get_actors()
get_movies()
