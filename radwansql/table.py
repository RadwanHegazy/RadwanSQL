"""
    Database Table Manager
"""
from .fields import *
import json
from .core import Tree, Metadata


class Table:

    __meta = Metadata()
    
    __avliable_fields = [
        IntegerField,
        StringField,
        FloatField,
        BoolField
    ]
    
    data = None
    fields = None
    _tid = None
    __tree = None

    def __init__(self) -> None:
        fields_values = self.fields.values()
        
        if len(fields_values) == 0:
            raise Exception("Please insert columns to your table")

        for fld in fields_values:
            if type(fld) not in self.__avliable_fields : 
                raise Exception(f"field type not supported")
        
        
    def __upload_data(self) :
        data = self.__read_bin()
        if self.__tree is None and len(data) >= 1:
            self.__tree = Tree(data.pop(0))
            for i in data:
                self.__tree.add_child(i)

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
        
        self.data = self.__tree.get_all_childs()
        self.__write_bin()
    
    def all(self) : 
        if self.__tree:
            self.data = self.__tree.get_all_childs() 
        else:
            self.data = self.__read_bin()
        return self.data

    def get (self, tid) :
        self.data = self.__tree.retrive_child(tid)
        return self
        
    
    def update (self, **data) :
        self.validate_keys(**data) 
        if self.__tree:
            self.__tree = self.__tree.update_child(self.data.get('_tid'), **data)
            self.data = self.__tree.retrive_child(self.data.get('_tid'))

        return self
    
    def delete(self):
        if self.__tree:
            self.__tree = self.__tree.delete(self.data.get('_tid'))
        self.__flush_db()
        self.data = self.__tree.get_all_childs()
        self.__write_bin()
        
    def export_as_json (self, name, indent=4) : 
        data = self.data
        file = open(f'{name}.json', 'w')
        file.write(json.dumps(data, indent=indent))

    def oldest(self) : 
        self.data = self.all()[0]
        return self

    def latest(self) :
        self.data = self.all()[-1]
        return self

    def __write_bin(self) : 
        readed_bin = self.__read_bin()

        if type(self.data) == dict:
            if type(readed_bin) == list:
                data = readed_bin + [self.data]
            elif type(readed_bin) == dict:
                data = [readed_bin] + [self.data]
                

        elif type(self.data) == list:
            data = readed_bin + self.data

        else:
            data = readed_bin

        self.__meta.write_data(data)
    
    def __flush_db(self) : 
        self.__meta.flush()

    def __read_bin(self) :
        return self.__meta.read_data()
    
    def update_db_name(self, name:str) :
        if not name.endswith(".rsql") :
            name = name + ".rsql"
        self.__meta.db_name = name
