"""
    Database Table Manager
"""
from fields import *
import json
from core import Tree

class Table:
    
    __avliable_fields = [
        IntegerField,
        StringField,
        FloatField,
        BoolField
    ]
    
    __tree = None
    data = None
    _tid = None
    fields = None

    def __init__(self) -> None:
        fields_values = self.fields.values()
        
        if len(fields_values) == 0:
            raise Exception("Please insert columns to your table")

        for fld in fields_values:
            if type(fld) not in self.__avliable_fields : 
                raise Exception(f"field not supported")

    def validate_keys(self, **fields) : 
        db_fields_keys = self.fields.keys()
        user_fields_keys = fields.keys()
        for u_keys in user_fields_keys :
            if u_keys not in db_fields_keys : 
                raise Exception(f"field '{u_keys}' not founded in the table fields")

    def create (self, **fields) :
        self.validate_keys(**fields)
        if self.__tree:
            self.__tree.add_child(fields)
        else:
            self.__tree = Tree(fields)
    
    def all(self) : 
        if self.__tree:
            self.data = self.__tree.get_all_childs() 
        return self.data

    def get (self, tid) :
        if self.__tree:
            self.data = self.__tree.retrive_child(tid)
        return self
    
    def update (self, **data) :
        self.validate_keys(**data) 
        if self.__tree:
            self.data = self.__tree.update_child(self.data.get('_tid'), **data)
        return self
    
    def delete(self):
        if self.__tree:
            self.__tree = self.__tree.delete(self.data.get('_tid'))
        return self
        
    def export_as_json (self, name, indent=4) : 
        data = self.data
        file = open(f'{name}.json', 'w')
        file.write(json.dumps(data, indent=indent))

    def oldest(self) : ...

    def latest(self) : ...        
