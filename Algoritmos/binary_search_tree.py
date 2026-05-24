def inorder_tree_walk(x):
    if x is not None:
        inorder_tree_walk(x.left)
        print(x.key)
        inorder_tree_walk(x.right)

def postorder_tree_walk(x):
    if x is not None:
        postorder_tree_walk(x.left)
        postorder_tree_walk(x.right)
        print(x.key)

def preorder_tree_walk(x):
    if x is not None:
        print(x.key)
        preorder_tree_walk(x.left)
        preorder_tree_walk(x.right)

def tree_search(x, k):
    if x is None or x.key == k:
        return x
    if k < x.key:
        return tree_search(x.left, k)
    else:
        return tree_search(x.right, k)

def iterative_tree_search(x, k):
    while x is not None and x.key != k:
        if k < x.key:
            x = x.left
        else:
            x = x.right
    return x


def tree_minimum(x):
    while x.left is not None:
        x = x.left
    return x

def tree_maximum(x):
    while x.right is not None:
        x = x.right
    return x

def tree_successor(x):
    if x.right is not None:
        return tree_minimum(x.right)
    y = x.parent
    while y is not None and x == y.right:
        x = y
        y = y.parent
    return y

def tree_predecessor(x):
    if x.left is not None:
        return tree_maximum(x.left)
    y = x.parent
    while y is not None and x == y.left:
        x = y
        y = y.parent
    return y 

def tree_insert(T,z):
    y = None
    x = T.root
    while x is not None:
        y = x
        if z.key < x.key:
            x = x.left
        else:
            x = x.right
    z.parent = y
    if y is None:
        T.root = z
    elif z.key < y.key:
        y.left = z
    else:
        y.right = z

def tree_delete(T,z):
    if z.left == None or z.right == None:
        y = z
    else:
        y = tree_successor(z)

    if y.left is not None:
        x = y.left
    else:
        x = y.right
    
    if x is not None:
        x.parent = y.parent
    
    if y.parent == None:
        T.root = x
    elif y == y.parent.left:
        y.parent.left = x
    else:
        y.parent.right = x
    
    if y != z:
        z.key = y.key
    
    return y


def transplant(T,u,v):
    if u.parent is None:
        T.root = v 
    elif u == u.parent.left:
        u.parent.left = v
    else: 
        u.p.right = v
    
    if v != None:
        v.parent = u.parent


def tree_delete_transplant(T,z):
    if z.left is None:
        transplant(T,z,z.right)
    elif z.right is None:
        transplant(T,z,z.left)
    else:
        y = tree_minimum(z.right)
        if y != z.right:
            transplant(T, y, y.right)
            y.right = z.right
            y.right.parent = y
        
        transplant(T,z,y)
        y.left = z.left
        y.left.parent = y
