"""
    Binary search tree data strcutre write here
"""

class Metadata: 

    def __init__(self, db_name='default.rsql', tid_max=100000) -> None:
        self.db_name = db_name
        self.tid_max = tid_max


class Tree:
    meta = Metadata()

    def __init__(self, data, tid=1) -> None:
        self.data = data
        self.tid = tid
        self.left = None
        self.right = None

    def add_child(self, data) :     
        tid = self.meta.tid_max - self.tid
        
        if tid > self.tid : 
            if self.right:
                self.right.add_child(data)
            else:
                new_tid = self.tid + 1
                self.right = Tree(data, tid=new_tid)

        if tid < self.tid:
            if self.left:
                self.left.add_child(data)
            else:
                new_tid = self.tid + 1
                self.left = Tree(data, tid=new_tid)
                
    def get_all_childs (self) :
        elements = []
        elements.append(self.data)

        if self.left : 
            elements += self.left.get_all_childs()

        if self.right:
            elements += self.right.get_all_childs()


        return elements
    
    def retrive_child(self, tid) :
        if tid == self.tid:
            return self

        if self.left:
            return self.left.retrive_child(tid)

        if self.right:
            return self.right.retrive_child(tid)
    
    def update_child(self, tid, data):
        child = self.retrive_child(tid)
        if child:
            child.data = data
            return child
        
    def find_maximum(self) : 
        r = self.right
        while r : 
            r = r.right
        return r
    
    def find_minimum(self) : 
        l = self.left
        while l :
            l = l.left
        return l
    
    def delete(self, tid):
        if tid < self.tid:
            if self.left:
                self.left = self.left.delete(tid)
        elif tid > self.tid:
            if self.right:
                self.right = self.right.delete(tid)
        else:
            if self.left is None:
                return self.right
            elif self.right is None:
                return self.left
            
            min_larger_node = self.right.find_minimum()
            self.data = min_larger_node.data
            self.tid = min_larger_node.tid  
            self.right = self.right.delete(min_larger_node.tid)

    
if __name__ == "__main__" : 
    tree = Tree({"name":"radwan"})
    tree.add_child(data={"name":"ibrahim"})
    tree.add_child(data={"name":"Khaled"})

    print(tree.retrive_child(1).data)
    new_tree = tree.update_child(1, {"name":"radwan", "age":19})
    print(new_tree.get_all_childs())
    new_tree = tree.delete(1)
    print(new_tree.get_all_childs())
