class RBNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.color = 1

class RBTree:
    def __init__(self):
        self.nil = RBNode(0)
        self.nil.red = False
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil
    
    def left_rotate(T,x):
        y = x.right
        x.right = y.left

        if y.left is not None:
            y.left.parent = x

        y.parent = x.parent

        if x.parent == None:
            T.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def right_rotate(T,x):
        y = x.left
        x.left = y.right

        if y.right is not None:
            y.right.parent = x
        
        y.parent = x.parent 

        if x.parent == None:
            T.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y


    def insert(self, val):

        # Ordinary Binary Search Insertion

        new_node = RBNode(val)

        new_node.parent = None

        new_node.left = self.nil

        new_node.right = self.nil

        new_node.red = True  # new node must be red



        parent = None

        current = self.root

        while current != self.nil:

            parent = current

            if new_node.val < current.val:

                current = current.left

            elif new_node.val > current.val:

                current = current.right

            else:

                return

        # Set the parent and insert the new node

        new_node.parent = parent

        if parent == None:

            self.root = new_node

        elif new_node.val < parent.val:

            parent.left = new_node

        else:

            parent.right = new_node

        # Fix the tree

        self.fix_insert(new_node)

    def fix_insert(self, new_node):

        while new_node != self.root and new_node.parent.red:

            if new_node.parent == new_node.parent.parent.right:

                u = new_node.parent.parent.left  # uncle

                if u.red:



                    u.red = False

                    new_node.parent.red = False

                    new_node.parent.parent.red = True

                    new_node = new_node.parent.parent

                else:

                    if new_node == new_node.parent.left:

                        new_node = new_node.parent

                        self.rotate_right(new_node)

                    new_node.parent.red = False

                    new_node.parent.parent.red = True

                    self.rotate_left(new_node.parent.parent)

            else:

                u = new_node.parent.parent.right  # uncle



                if u.red:

                    u.red = False

                    new_node.parent.red = False

                    new_node.parent.parent.red = True

                    new_node = new_node.parent.parent

                else:

                    if new_node == new_node.parent.right:

                        new_node = new_node.parent

                        self.rotate_left(new_node)

                    new_node.parent.red = False

                    new_node.parent.parent.red = True

                    self.rotate_right(new_node.parent.parent)

        self.root.red = False

