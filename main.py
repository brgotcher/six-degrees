import requests

KEY = "fd1ba63489529c937b3759165608f6cd"

# x = requests.get("https://api.themoviedb.org/3/person/1/movie_credits?api_key=fd1ba63489529c937b3759165608f6cd").json()
# movies = x["cast"]
# list = []
# for movie in movies:
#     list.append(movie["title"])
#
# print(list)


a = open("actors.txt", "w")
for i in range(99999):
    try:
        req = requests.get("https://api.themoviedb.org/3/person/" + str(i) + "/movie_credits?api_key=fd1ba63489529c937b3759165608f6cd", timeout=20)
        list = []
        if req.status_code == 200:
            req = req.json()
            movies = req["cast"]
            for movie in movies:
                list.append(movie["id"])
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

m = open("movies.txt", "w")
for i in range(99999):
    try:
        req = requests.get("https://api.themoviedb.org/3/movie/" + str(i) + "/credits?api_key=fd1ba63489529c937b3759165608f6cd", timeout=20)
        list = []
        if req.status_code == 200:
            req = req.json()
            cast = req["cast"]
            for actor in cast:
                list.append(actor["id"])
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

m.close()


    # print()
    # print("=========================================================================================")
    # print(i)
    # print("=========================================================================================")
    # print(req)
    # print()
    # movies = req["cast"]
    # list = []
    # for movie in movies:
    #     list.append(movie["title"])
    # print(i)
    # print(list)