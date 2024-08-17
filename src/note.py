class Note:
    def __init__(self, title, content):
        self.title = title
        self.content = self.format_note(content)
        self.created_at = None
        self.modified_at = None
        self.tags = []


    def __str__(self):
        return self.content

    @staticmethod
    def format_note(note, line_length=50):
        """Format the note to have new lines every `line_length` characters."""
        return '\n'.join([note[i:i + line_length] for i in range(0, len(note), line_length)])

    def add_tag_to_note(self):
        pass
