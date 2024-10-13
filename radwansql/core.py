"""
    Binary search tree data strcutre write here
"""
import pickle, os

class Metadata: 

    def __init__(self, db_name='default.rsql', tid_max=100000) -> None:
        self.db_name = db_name
        self.tid_max = tid_max


    def write_data(self, data) :
        with open(self.db_name, 'wb') as p_file :
            pickle.dump(data, p_file)
    
    def flush(self) : 
        os.remove(self.db_name)
        
    def read_data(self) : 
        try : 
            with open(self.db_name, 'rb') as p_file : 
                data = pickle.load(p_file)
        except FileNotFoundError:
            data = []
        return data

class Tree:
    meta = Metadata()

    def __init__(self, data=[], tid=1) -> None:
        self.data = data
        self.tid = tid
        self.left = None
        self.right = None

    def represent_data (self, data):
        output = None
        if type(data) == list:
            output = []
            for i in data:
                output.append({
                '_tid' : self.tid,
                **i
            })
                
        elif type(data) == dict:
            output = {
                '_tid' : self.tid,
                **data
            }
        return output
    
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
        elements.append(self.represent_data(self.data))

        if self.left : 
            elements += self.left.get_all_childs()

        if self.right:
            elements += self.right.get_all_childs()


        return elements
    
    def retrive_child_object(self, tid) :
        if tid == self.tid:
            return self

        if self.left:
            return self.left.retrive_child(tid)

        if self.right:
            return self.right.retrive_child(tid)
    
    def retrive_child(self, tid) :
        if tid == self.tid:
            return self.represent_data(self.data)

        if self.left:
            return self.left.retrive_child(tid)

        if self.right:
            return self.right.retrive_child(tid)
    
    def update_child(self, tid, **data):
        child = self.retrive_child_object(tid)
        if child:
            original_data = child.data
            for k, v in data.items() :
                original_data[k] = v
            child.data = original_data
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
