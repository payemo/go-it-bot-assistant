import hashlib
import os
import pickle
import sys
from collections import UserDict


class DataManager:
    def __init__(self):
        """Initiates DataManager object and creates filename parameter"""
        self.filename = self.auth()

    def save_data(self, database):
        """
        Save the data in a pickle file.
        :param database: Database object to save.
        """
        with open(self.filename, "wb") as f:
            pickle.dump(database, f)

    def load_data(self):
        """
        Load the data from a pickle file or to create a new AddressBook object.
        """
        try:
            with open(self.filename, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            # TODO
            pass
            #return AddressBook()

    @staticmethod
    def generate_hash(email: str, password: str) -> str:
        """
        Generate a filename based on the email and password.
        :param email: user`s email from input
        :param password: user`s password from input
        :return:
        """
        hash_obj = hashlib.sha256(email.encode() + password.encode())
        return hash_obj.hexdigest()

    def validate_secret(self) -> str:
        """
        Taking 2 passwords from input and check if they are same.
        :return: Password(str)
        """
        pwd = input("Enter password: ")
        conf_pwd = input("Confirm password: ")
        if conf_pwd == pwd:
            return pwd
        else:
            print("Passwords are not identical! Try one more time please.\n")
            self.validate_secret()

    def signup(self):
        """
        Input of email and password.
        :return: hashed email + password
        """
        email = input("Enter email address: ")
        pwd = self.validate_secret()
        file_name = self.generate_hash(email, pwd)
        print("You have registered successfully!")
        return file_name

    def login(self):
        """
        Input of email and password. If such pair already exists - create and return filename.
        Through to main menu if it does not exist.
        :return: hashed email + password
        """
        email = input("Enter email: ")
        pwd = input("Enter password: ")
        secret_hash = self.generate_hash(email, pwd)

        if not os.path.exists(secret_hash):
            print("User with such email or password does not exist!")
            secret_hash = self.auth()
        else:
            print("Logged in Successfully!")
        return secret_hash

    def auth(self) -> bool:
        """
        Filename handling function
        :return: filename or exit the program
        """
        print(
            """What would you like to do?
                    1.Signup
                    2.Login
                    3.Exit
            """
        )
        choice = int(input("Enter your choice: "))
        if choice == 1:
            file_name = self.signup()
        elif choice == 2:
            file_name = self.login()
            if not file_name:
                self.auth()
        elif choice == 3:
            print("Exiting...")
            sys.exit()
        else:
            print("Wrong Choice!")
            file_name = self.auth()

        return file_name
