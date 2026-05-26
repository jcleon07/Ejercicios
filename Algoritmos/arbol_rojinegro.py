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
