class Field:
    def __init__(self, value) -> None:
        self._validate(value)
        self._value = value

    def __str__(self) -> str:
        return str(self._value)
    
    def _validate(self, value: str):
        raise NotImplementedError(f"[Field.{self._validate.__name__}] not implemented.")
    
class Name(Field):
    def _validate(self, value: str):
        pass
    
class Phone(Field):
    def _validate(self, value: str):
        pass

class Address(Field):
    def _validate(self, value: str):
        pass

class Email(Field):
    def _validate(self, value: str):
        pass

class Birthday(Field):
    def _validate(self, value: str):
        pass