from abc import ABC, abstractmethod
from fuzzywuzzy import fuzz

from notes import NoteRecord
from main_module import main


class GetInfo(ABC):

    @abstractmethod
    def show_info(self):
        pass

    @abstractmethod
    def find_info(self):
        pass


class GetAddressBook(GetInfo):
    def show_info(self):
        main().address_book.__str__()

    def find_info(self):
        main().address_book.find_contact(main().sep_command[2].title())


class GetNotes(GetInfo):
    def show_info(self):
        print(f"Total notes: {NoteRecord.counter}")
        if not main().note_list:
            print("List with notes is empty.")
        for note in main().note_list:
            print(f"Title: {note['title']}\nNote: {note['note']}\nTag: {note['tag']}\n")

    def find_info(self):
        for note in main().note_list:
            rat_of_string = fuzz.WRatio(note['note'], ' '.join(main().sep_command[2:]))
            if rat_of_string > 50:
                print(f"Title: {note['note']}\nNote: {note['note']}\n")


class GetHelpInfo(GetInfo):
    def show_info(self):
        """
        =====================================================
                     CLI - Command Line Interface
                           Personal Assistant
        =====================================================

        Personal Assistant works with Address book, write,
        save Notes and sort files in folders.

        Personal Assistant has a commands:
        1. "add contact" - for add name, contact information
        (phone, e-mail), birthday and address to Address book
        write "add contact" and enter command then Assistant
        ask you details enter it;

        2. "add note" - for add note write "add note" then
        your note after write "-title" and title for your note
        and enter it; additionally in this option you can add
        a tag to your note for this after title write "-tag"
        and tag and enter it;

        3. "add tag" - for add tag to notes write "add tag"
        then write tag after write "-title" and title of note
        which you wont to add tag and enter it;

        4. "show contact" - for get all contact information
        write "show contact" then name and enter it;

        5. "show birthday" - for show a list of contacts who
        have a birthday after a specified number of days from
        the current date write "show birthday" then number of
        days and enter it;

        6. "show all" - for show all contacts in Address book
        write "show all" and enter command;

        7. "show notes" - for show all notes write "show notes"
        and enter it;

        8. "edit contact" - for edit contact information write
        "edit contact" and enter command then Assistant ask
        name enter it;

        9. "edit note" - for edit note write "edit note" then
        title after write "-edit" and new text and enter it;

        10. "search tags" - for search and sort notes by tags
        write "search tags" then tag and enter it;

        11. "search note" - for search note in notes write
        "search note" then few words from note and enter it;

        12. "sort folders" - for sort files in folders write
        "sort folders" then path to folder and enter it;

        13. "delete contact" - for delete name and contact
        information in Address book write "delete contact" then
        name and enter it;

        14. "delete note" - for delete note write "delete note"
        then title and enter it;

        15. "help", "reference" - for ask reference how to
        use Personal Assistant write "help" or "reference"
        and enter the command;

        16. "close", "exit", "good bye" - for finish work with
        Personal Assistant, write one of "close", "exit" or
        "good bye" and enter command then you will exit from
        Command Line Interface.

        Pleasant use!
        """
        print(self.show_info.__doc__)

    def find_info(self):
        pass
