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
        self.num_of_nodes = 0

    def insert(self, root, id, src):
        # compare actor_id to root, move left or right or return if equal
        if not root:
            self.num_of_nodes += 1
            return Node(id, src)
        elif id < root.id:
            root.left = self.insert(root.left, id, src)
        elif id > root.id:
            root.right = self.insert(root.right, id, src)
        else:
            return root

        # adjust height for balancing
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        # check balance and rotate if needed
        balance = self.get_balance(root)
        if balance > 1:
            if id < root.left.id:
                return self.right_rotate(root)
            else:
                root.left = self.left_rotate(root.left)
                return self.right_rotate(root)
        if balance < -1:
            if id > root.right.id:
                return self.left_rotate(root)
            else:
                root.right = self.right_rotate(root.right)
                return self.left_rotate(root)
        return root

    def left_rotate(self, node):
        new_root = node.right
        child = new_root.left
        new_root.left = node
        node.right = child
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        new_root.height = 1 + max(self.get_height(new_root.left), self.get_height(new_root.right))
        return new_root

    def right_rotate(self, node):
        new_root = node.left
        child = new_root.right
        new_root.right = node
        node.left = child
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))
        new_root.height = 1 + max(self.get_height(new_root.left), self.get_height(new_root.right))
        return new_root

    def get_height(self, root):
        if not root:
            return 0
        return root.height

    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    # print an in-order traversal of the tree
    def print_tree(self, root):
        if not root:
            return

        self.print_tree(root.left)
        print(root.id, end=" ")
        self.print_tree(root.right)

    def get_in_order_array(self, root, arr):
        if not root:
            return

        self.get_in_order_array(root.left, arr)
        arr.append(root.id)
        self.get_in_order_array(root.right, arr)

    def search(self, root, id):
        if not root:
            return None

        if id < root.id:
            return self.search(root.left, id)
        elif id > root.id:
            return self.search(root.right, id)
        else:
            return root

