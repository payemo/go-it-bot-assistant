# Telephone Book and Notes Assistant

CLI system for storing and interacting with address book entries and notes with an option of adding Tags to notes. The app also has a simple authentication system, that allows to have separate 'databases'.


## Installing / Getting started

A quick introduction of the minimal setup you need to get Assistant app up &
running.

### Python3 must be already installed!

Linux/macOS
```shell
git clone https://github.com/payemo/go-it-bot-assistant/
cd go-it-bot-assistant
python3 -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
```

Installation on Windows
```shell
git clone https://github.com/payemo/go-it-bot-assistant/
cd go-it-bot-assistant
python -m venv venv 
venv\Scripts\activate
pip install -r requirements.txt
```

### Or using setup.py file

For Linux/macOS
```shell
git clone https://github.com/payemo/go-it-bot-assistant/
cd go-it-bot-assistant
python3 setup.py install
```

For Windows
```shell
git clone https://github.com/payemo/go-it-bot-assistant/
cd go-it-bot-assistant
python setup.py install
```

## Features:
1. Telephone Book Management
 - Add Contacts: Easily add new contacts to your telephone book with name, phone numbers, email, and other details.
 - View Contacts: Display a list of all contacts.
 - Edit Contacts: Update existing contact information to keep your telephone book up to date.
 - Delete Contacts: Remove outdated or incorrect contacts from your telephone book.
 - Search Contacts: Quickly search for contacts by name, phone number or email.
2. Note-Taking
- Create Notes: Capture important information by creating notes with titles and content.
- View Notes: List all notes or view a specific note by its title.
- Edit Notes: Update the content of your existing notes to reflect new information or changes.
- Delete Notes: Remove notes that are no longer needed.
3. Tagging System
- Add Tags to Notes: Organize your notes by adding tags for easy categorization.
- Remove Tags: Edit the tags associated with a note to ensure they accurately reflect the content.
4. User-Friendly CLI
- Intuitive Commands: The CLI is designed with user-friendly commands and options to make navigation and operation simple.
- Help and Documentation: Access help commands to guide you through the available features and how to use them effectively.
5. Data Persistence
- Basic Authentication Mechanism: Signup and login to create separate accounts, allowing for distinct, private databases for each user.
- Save and Load Data: Automatically save your telephone book records and notes to a file, ensuring your data is persistent across sessions.

