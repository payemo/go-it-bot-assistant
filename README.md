# Telephone Book and Notes Assistant

CLI system for storing and interacting with address book entries and notes with an option of adding Tags to notes. The app also has a simple authentication system, that allows to have separate 'databases'.
## Installing / Getting started
A quick introduction of the minimal setup you need to get Assistant app up & running.
### Python3 must be already installed!
#### Linux/macOS

```
git clone https://github.com/payemo/go-it-bot-assistant/
cd go-it-bot-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
#### Windows

```
git clone https://github.com/payemo/go-it-bot-assistant/
cd go-it-bot-assistant
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Installation via `setup.py`
#### Linux/macOS

```
git clone https://github.com/payemo/go-it-bot-assistant/
cd go-it-bot-assistant
python3 setup.py install
```
#### Windows

```
git clone https://github.com/payemo/go-it-bot-assistant/
cd go-it-bot-assistant
python setup.py install
```

## Features:

### Telephone Book Management

| Title                   | Command               | Description                                                                                           |
| ----------------------- | --------------------- | ----------------------------------------------------------------------------------------------------- |
| Add contacts            | `add-record`          | Adds new contacts to your telephone book with name, phone numbers, email, and other details.          |
| Search contacts         | `search-record`       | Quickly search for contacts by name, phone number or email.                                           |
| View contacts           | `show-all-records`    | Display a list of all contacts.                                                                       |
| Delete contacts         | `remove-record`       | Remove outdated or incorrect contacts from your telephone book.                                       |
| Adding additional phone | `add-phone`           | Adds additional phone number for the specified user. *There are could be duplicates in a phone book.* |
| Delete phone            | `remove-phone`        | Removes phone from address book.                                                                      |
| Show upcoming birthdays | `show-upcoming-bdays` | Output upcoming birthday for the next week.                                                           |
| Show record notes       | `show-record-notes`   | Displays list of notes of a specified contact.                                                        |
#### Note-Taking
Notes are independent entities but there is an option to link note to the record. In that case the same notes are *living* in a system but behave independently. Any changes made to either record's note or *global* notes except **tag renaming** are not interchangeable.

| Title             | Command                                                                            | Description                                                                                                                                      |
| ----------------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| Create notes      | `add-note`                                                                         | Add new note. It's possible to type a multiline text. Also, it prompts user to link tag for the note and create a new one if such doesn't exist. |
| Edit notes        | `edit-note`                                                                        | Prompts user to enter note's title (which assumed to be unique) and edit either *title* or *content* of a specified note.                        |
| Delete note       | `remove-note`                                                                      | Remove **global** note from the list.                                                                                                            |
| Show note         | `show-note`                                                                        | Shows note's information (Title \| Content \| Tags \| Created \| Modified).                                                                      |
| Show notes        | `show-notes`                                                                       | Displays information about all existing *global* notes.                                                                                          |
| Searching note    | - `find-notes-by-date`<br>- `find-notes-by-word-in-title`<br>- `find-notes-by-tag` | Searching for notes by specified criteria.                                                                                                       |
| Link note         | `link-note`                                                                        | Links note to the specified record.                                                                                                              |
| Sort notes by tag | `sort-notes-by-tag`                                                                | Sorts all **global** notes by input tag.                                                                                                         |
#### Tagging System
The same as `Note` entities, `Tag` *lives* in a system independently. Any changes made to **tag** are applied to **list of tags in notes and record's notes**.

| Title      | Command      | Description                                                                                                 |
| ---------- | ------------ | ----------------------------------------------------------------------------------------------------------- |
| Create tag | `create-tag` | Creates a new tag.                                                                                          |
| Delete tag | `remove-tag` | Removes tag from a list. <br>*If a deleted tag was linked to a note then cascade deleting will be applied.* |
| Edit tag   | `edit-tag`   | Edits the title of a specified tag.                                                                         |
| Link tag   | `link-tag`   | Links tag to a specified **global** note.                                                                   |
| Show tags  | `show-tags`  | Displays the list of all tags.                                                                              |

#### User-Friendly CLI
- Intuitive Commands: The CLI is designed with user-friendly commands and options to make navigation and operation simple.
- Help and Documentation: Access help commands to guide you through the available features and how to use them effectively.
#### Data Persistence
- Basic Authentication Mechanism: Signup and login to create separate accounts, allowing for distinct, private databases for each user.
- Save and Load Data: Automatically save your telephone book records and notes to a file, ensuring your data is persistent across sessions.