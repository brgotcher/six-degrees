import requests
import linecache

KEY = "fd1ba63489529c937b3759165608f6cd"


class Node:
    def __init__(self, id, src):
        self.id = int(id)
        self.left = None
        self.right = None
        self.height = 1
        # source variable to trace back the path when a connection is found
        self.src = src


class Tree:
    def __init__(self):
        self.root = None

    def insert(self, root, id, src):
        # compare id to root, move left or right or return if equal
        if not root:
            return Node(id, src)
        elif id < root.id:
            root.left = self.insert(root.left, id, src)
        elif id > root.id:
            root.right = self.insert(root.right, id, src)
        else:
            return root

        # adjust height for balancing
        root.height = 1 + max(self.getHeight(root.left), self.getHeight(root.right))
        # check balance and rotate if needed
        balance = self.getBalance(root)
        if balance > 1:
            if id < root.left.id:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if balance < -1:
            if id > root.right.id:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
        return root

    def leftRotate(self, node):
        newRoot = node.right
        child = newRoot.left
        newRoot.left = node
        node.right = child
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))
        newRoot.height = 1 + max(self.getHeight(newRoot.left), self.getHeight(newRoot.right))
        return newRoot

    def rightRotate(self, node):
        newRoot = node.left
        child = newRoot.right
        newRoot.right = node
        node.left = child
        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))
        newRoot.height = 1 + max(self.getHeight(newRoot.left), self.getHeight(newRoot.right))
        return newRoot

    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)

    # print an in-order traversal of the tree
    def printTree(self, root):
        if not root:
            return

        self.printTree(root.left)
        print(root.id, end=" ")
        self.printTree(root.right)

    def getInOrderArray(self, root, arr):
        if not root:
            return

        self.getInOrderArray(root.left, arr)
        arr.append(root.id)
        self.getInOrderArray(root.right, arr)

    def search(self, root, id):
        if not root:
            return None

        if id < root.id:
            return self.search(root.left, id)
        elif id > root.id:
            return self.search(root.right, id)
        else:
            return root

def getActorIDFromName(name):
    name = name.replace(" ", "+")
    details = requests.get("https://api.themoviedb.org/3/search/person?api_key=" + KEY + "&query=" + name)
    details = details.json()
    name = str(details["results"][0]["id"])
    return name

def getMovieList(id):
    movies = linecache.getline("actors.txt", id)
    movies = movies[1:-2]
    movies = movies.split(", ")
    for i in range(0, len(movies)):
        movies[i] = int(movies[i])
    return movies

def getCastList(id):
    cast = linecache.getline("movies.txt", id)
    cast = cast[1:-2]
    cast = cast.split(", ")
    for i in range(0, len(cast)):
        cast[i] = int(cast[i])
    return cast

def getMovieNameFromID(id):
    data = requests.get("https://api.themoviedb.org/3/movie/" + str(id) + "?api_key=fd1ba63489529c937b3759165608f6cd")
    data = data.json()
    title = data["title"]
    return title

def getActorNameFromID(id):
    data = requests.get("https://api.themoviedb.org/3/person/" + str(id) + "?api_key=fd1ba63489529c937b3759165608f6cd")
    data = data.json()
    name = data["name"]
    return name

def checkConnections(actors, aTree, aRoot, mTree, mRoot, count, target):
    if count >= 5:
        return -1
    newActorList = []
    for actor in actors:
        if actor > 99999:
            continue
        newMovieList = []
        movieList = getMovieList(actor)
        for movie in movieList:
            if movie > 85419:
                continue
            # if movie not in movies and movie not in newMovieList:
            if not mTree.search(mRoot, movie):
                newMovieList.append(movie)
                mRoot = mTree.insert(mRoot, movie, actor)
        for movie in newMovieList:
            actorList = getCastList(movie)
            for actr in actorList:
                if actr > 99998:
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

# print(getMovieList(536))
#
# data = requests.get("https://api.themoviedb.org/3/person/536/movie_credits?api_key=" + KEY)
# data = data.json()
# data = data["cast"]
# movieList = []
# for movie in data:
#     movieList.append(movie["id"])
# print(movieList)

actorTree = Tree()
movieTree = Tree()
actorRoot = None
movieRoot = None

actor1 = input("Enter an actor: ")
actor1 = int(getActorIDFromName(actor1))
while actor1 > 99998:
    actor1 = input("That actor is not yet available.  Please try another: ")
    actor1 = int(getActorIDFromName(actor1))
actor2 = input("Enter an actor: ")
actor2 = int(getActorIDFromName(actor2))
while actor2 > 99998:
    actor2 = input("That actor is not yet available.  Please try another: ")
    actor2 = int(getActorIDFromName())


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