from datetime import datetime, timedelta

class Field:
    def __init__(self, value) -> None:
        self._validate(value)
        self._value = value

    def __str__(self) -> str:
        return str(self._value)
    
    def _validate(self, value: str):
        raise NotImplementedError(f"[Field.{self._validate.__name__}] not implemented.")
    
class Name(Field):
    def __init__(self, value) -> None:
        self._validate(value)
        self._value = value

    def _validate(self, value: str):
        pass
    
class Phone(Field):
    required_num_of_digits = 10

    def __init__(self, value) -> None:
        self._validate(value)
        self._value = value

    def __str__(self) -> str:
        return str(self._value)
    
    def _validate(self, value: str):
        try:
            if int(value) and len(value) != Phone.required_num_of_digits:
                raise ValueError("Phone not equals 10 digits")
        except:
            raise ValueError("All characters are not digits")
        

class Address(Field):
    def __init__(self, value) -> None:
        self._validate(value)
        self._value = value

    def _validate(self, value: str):
        pass

class Email(Field):
    def __init__(self, value) -> None:
        self._validate(value)
        self._value = value

    def __str__(self) -> str:
        return str(self._value)

    def _validate(self, value: str):
        pass

class Birthday(Field):
    def __init__(self, value) -> None:
        self._validate(value)
        self._value = value

    def __str__(self) -> str:
        return str(self._value)

    def _validate(self, value: str):
        try:
            date = datetime.strptime(value, "%d.%m.%Y").date()
            if date > datetime.today().date():
                raise ValueError("Birthdate is from the future")
        except:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")