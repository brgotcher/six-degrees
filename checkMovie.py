import requests

cont = 1
while cont == 1:
    movID = input("Enter a movie ID")
    data = requests.get("https://api.themoviedb.org/3/movie/" + str(movID) + "?api_key=fd1ba63489529c937b3759165608f6cd")
    if data.status_code == 200:
        data = data.json()
        name = data["title"]
        print(name)
    else:
        print("Movie not found")
    cont = int(input("Check another movie? Enter 1 to continue"))