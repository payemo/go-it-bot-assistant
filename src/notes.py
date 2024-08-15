class Note:
    def __init__(self, content):
        self.content = self.format_note(content)

    def edit(self, new_content):
        self.content = self.format_note(new_content)
        return f"Note updated to: {self.content}"

    @staticmethod
    def format_note(note, line_length=50):
        """Format the note to have new lines every `line_length` characters."""
        return '\n'.join([note[i:i + line_length] for i in range(0, len(note), line_length)])

    def __str__(self):
        return self.content


class NotesManager:
    def __init__(self):
        self.notes = []

    def add_note(self, content):
        note = Note(content)
        self.notes.append(note)
        return f"Note added: {note}"

    def remove_note(self, content):
        for note in self.notes:
            if note.content == content:
                self.notes.remove(note)
                return f"Note removed: {note.content}"
        return "Note not found."

    def edit_note(self, old_content, new_content):
        for note in self.notes:
            if note.content == old_content:
                return note.edit(new_content)
        return "Note not found."

    def show_notes(self):
        if not self.notes:
            return "No notes available."
        return '\n\n'.join(str(note) for note in self.notes)