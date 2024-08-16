class Note:
    def __init__(self, content):
        self.content = self.format_note(content)

    def edit(self, new_content):
        self.content = self.format_note(new_content)
        return f"Note updated to: {self.content}"

    def search_notes_by_tag(self, tag):
        return [note for note in self.notes if tag in note.tags]

    def sort_notes_by_tag(self):
        return sorted(self.notes, key=lambda note: ', '.join(note.tags))

    def display_notes(self):
        for note in self.notes:
            print(f"\nAuthor: Edd\nTitle: {note.title}\nNote: {note.content}\nTags: {'; '.join(note.tags)}\nCreated at: {note.created_at.strftime('%a %d %b %Y, %I:%M%p')}\n")

    @staticmethod
    def format_note(note, line_length=50):
        """Format the note to have new lines every `line_length` characters."""
        return '\n'.join([note[i:i + line_length] for i in range(0, len(note), line_length)])

    def __str__(self):
        return self.content
    
    def add_note(self):
        title = input("Enter title: ")
        content = input("Enter body: ")
        tags = []
        while True:
            tag = input("Enter tag (n=close): ")
            if tag == 'n':
                break
            tags.append(tag)
        note = Note(title, content, tags)
        # need to add note
        
        print("Note added.")
