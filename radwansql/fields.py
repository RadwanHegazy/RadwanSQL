"""
    Field and field types for my sql
"""
from abc import ABC, abstractmethod

__all__ = [
    "StringField",
    "IntegerField",
    "FloatField",
    "BoolField",
]

class BaseField:
    """this is the base object for other fields

    Raises:
        Exception: for any exception just call self._error("<YOUR_ERROR_MSG>")

    Returns:
        _type_: None
    """
    _type = None
    _val = None

    def __init__(self, default=None, required=True) -> None:
        self.default = default
        self.required = required

    @abstractmethod
    def validate(self) : 
        """for validate enterd value from user depends on class kwargs

        Returns:
            _type_: return the enterd value after validation
        """
        value = self._val
        if self._val is None and self.required:
            if self.default:
                value = self.default
            else:
                self._error('Field is required')
        return value

    def set_value(self, val=None) :
        if val is None:
            val = self.default 
        self._val = self._type(val)
        self._val = self.validate()

    def get_value(self) : 
        return self._val
    
    def _error(self, er) : 
        raise Exception(er)


class StringField (BaseField) : 
    _type = str

    def __init__(self,max_len=None,min_len=None,default=None, required=True) -> None:
        self.max_len = max_len
        self.min_len = min_len
        super().__init__(default, required)
    
    def validate(self):
        
        value = super().validate()
        if self.max_len :
            if len(value) > self.max_len :
                self._error(f"Max length should be less than {self.max_len}")
        
        if self.min_len:
            if len(value) < self.min_len:
                self._error(f"Min length should be greater than {self.min_len}")

        return value
    

class IntegerField(BaseField) : 
    _type = int
    
    def __init__(self,max_num=None, min_num=None, default=None, required=True) -> None:
        self.max_num = max_num
        self.min_num = min_num
        super().__init__(default, required)

    def validate(self):
        value = super().validate()
        
        if self.max_num :
            if value > self.max_num :
                self._error(f"value should be less than {self.max_num}, you typed {value}")
            
        if self.min_num:
            if value < self.min_num : 
                self._error(f"value should be greater than {self.min_num}, you typed {value}")

        return value


class FloatField (IntegerField) :
    _type = float

    def __init__(self, digits=None,max_num=None, min_num=None, default=None, required=True) -> None:
        self.digits = digits
        super().__init__(max_num, min_num, default, required)

    def validate(self):
        value =  super().validate()
        if self.digits : 
            value = round(value, self.digits)
        return value


class BoolField (BaseField) : 
    _type = bool

    def validate(self):
        return super().validate()
