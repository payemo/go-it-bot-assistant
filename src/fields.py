from datetime import datetime, timedelta
import re

class Field:
    def __init__(self, value) -> None:
        self._value = self._validate(value)

    def __str__(self) -> str:
        return str(self._value)
    
    def __eq__(self, other) -> bool:
        return self._value == other.__value
    
    def _validate(self, value: str):
        raise NotImplementedError(f"[Field.{self._validate.__name__}] not implemented.")
    
    @property
    def value(self):
        return self._value
    
class Name(Field):
    def _validate(self, value: str):
        return value
    
    # Able to use that class as key for hash structures.
    def __hash__(self) -> int:
        return hash(self._value)
    
class Phone(Field):
    required_num_of_digits = 10

    def _validate(self, value: str):
        if not value.isdigit():
            raise ValueError("All characters are not digits")
        if len(value) != self.required_num_of_digits:
            raise ValueError(f"Phone number must be {self.required_num_of_digits} digits long")
        return value
        

class Address(Field):
    def _validate(self, value: str):
        return value

class Email(Field):
    def _validate(self, value: str):
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, value):
            raise ValueError(f"{value} - email address format is invalid")
        return value

class Birthday(Field):
    def _validate(self, value: str):
        try:
            date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        
        if date > datetime.today().date():
            raise ValueError("Birthdate is from the future")
        return date