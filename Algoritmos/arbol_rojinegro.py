class RBNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.color = 0

class RBTree:
    def __init__(self):
        self.nil = RBNode(0)
        self.nil.red = False
        self.nil.left = None
        self.nil.right = None
        self.root = self.nil
    
    def left_rotate(self, x):
        y = x.right
        x.right = y.left

        if y.left is not None:
            y.left.parent = x

        y.parent = x.parent

        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y

        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right

        if y.right is not None:
            y.right.parent = x
        
        y.parent = x.parent 

        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y

        y.right = x
        x.parent = y


        

    def insert(self, z):
        y = self.nil
        x = self.root
        
        while x != self.nil:
            y = x

            if z.key == x.key:
                x = x.left
            else:
                x.right
        z.parent = y

        if y == self.nil:
            self.root = z
        elif z.key < y.key:
            y.left = z
        else:
            y.right = z

        z.left = self.nil
        z.right = self.nil
        z.color = 1
        self.insert_fixup(self,z)

    def insert_fixup(self, z):
        while z.parent.color == 1:
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right

                if y.color == 1:
                    z.parent.color = 0
                    y.color = 0
                    z.parent.parent.color = 1 
                    z = z.parent.parent
                elif z == z.parent.right:
                    z = z.parent
                    self.left_rotate(self,z)

                z.parent.color = 0
                z.parent.parent.color = 1
                self.right_rotate(self, z.parent.parent)
            
            else:
                y = z.parent.parent.left

                if y.color == 1:
                    z.parent.color = 0
                    y.color = 0
                    z.parent.parent.color = 1
                    z = z.parent.parent
                elif z == z.parent.left:
                    z = z.parent
                    self.right_rotate(self,z)

                z.parent.color = 0
                z.parent.parent.color = 1
                self.left_rotate(self, z.parent.parent)

        self.root.color = 0

    def transplant(self, u, v):
        if u.parent == self.nil:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        v.parent = u.parent 

    def tree_minimum(x):
        while x.left != None:
            x = x.left

        return x

    def delete(self, z):
        y = z
        y_original_color = y.color

        if z.left == self.nil:
            x = z.right
            self.transplant(self, z, z.right)
        elif z.right == self.nil:
            x = z.left
            self.transplant(self, z, z.left)
        else:
            y = self.tree_minimum(z.right)
            y_original_color = y.color
            x = y.right

            if y != z.right:
                self.transplant(self, y, y.right)
                y.right = z.right
                y.right.parent = y
            else:
                x.parent = y 
            
            self.transplant(self, z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        
        if y_original_color == 0:
            self.delete_fixup(self, x)

    def delete_fixup(self, x):
        if x == x.parent.left:
            w = x.parent.right

            if w.color == 1:
                w.color = 0
                x.parent.color = 1
                self.left_rotate(self, x.parent)
                w = x.parent.right

            if w.left.color == 0 and w.right.color == 0:
                w.color = 1
                x = x.parent
            else:
                if w.right.color == 0:
                    w.left.color = 0
                    w.color = 1
                    self.right_rotate(self, w)
                    w = x.parent.right
                
                w.color = x.parent.color
                x.parent.color = 0
                w.right.color = 0
                self.left_rotate(self, x.parent)
                x = self.root
        
        else:
            w = x.parent.left

            if w.color == 1:
                w.color = 0
                x.parent.color = 1
                self.right_rotate(self, x.parent)
                w = x.parent.left

            if w.right.color == 0 and w.left.color == 0:
                w.color = 1
                x = x.parent
            else:
                if w.left.color == 0:
                    w.right.color = 0
                    w.color = 1
                    self.left_rotate(self, w)
                    w = x.parent.left
                
                w.color = x.parent.color
                x.parent.color = 0
                w.left.color = 0
                self.right_rotate(self, x.parent)
                x = self.root
                
        x.color = 0