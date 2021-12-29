import requests

cont = 1
while cont == 1:
    actID = input("Enter an actor ID")
    data = requests.get("https://api.themoviedb.org/3/person/" + str(actID) + "?api_key=fd1ba63489529c937b3759165608f6cd")
    if data.status_code == 200:
        data = data.json()
        name = data["name"]
        print(name)
    else:
        print("Actor not found")
    cont = int(input("Check another actor? Enter 1 to continue"))