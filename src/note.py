import copy
from datetime import datetime

class Note:
    def __init__(self, title, content):
        self.title = title
        self.content = self.format_note(content)
        self.created_at = datetime.now()
        self.modified_at = None
        self.tags = []

    def __str__(self):
        return f"{self.title} : {self.content}"
    
    def __copy__(self):
        cls = self.__class__
        cpy = cls.__new__(cls)
        cpy.__dict__.update(self.__dict__)
        # Let just move tags without creating new copy
        cpy.tags = copy.copy(self.tags)
        return cpy

    @staticmethod
    def format_note(note, line_length=50):
        """Format the note to have new lines every `line_length` characters."""
        return '\n'.join([note[i:i + line_length] for i in range(0, len(note), line_length)])
