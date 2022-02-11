import requests

KEY = "fd1ba63489529c937b3759165608f6cd"

data = requests.get("https://api.themoviedb.org/3/search/person?api_key=" + KEY + "&query=Farel")
data = data.json()
data = data["results"]
results = []
for res in data:
    (name, id) = (res["name"], res["actor_id"])
    print(name + ": " + str(id))
