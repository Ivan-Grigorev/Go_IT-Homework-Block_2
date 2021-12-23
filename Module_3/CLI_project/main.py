import difflib
import json
import pickle
from fuzzywuzzy import fuzz

from address_book import AddressBook, Record
from notes import NoteRecord
from sort_folder import sort_folder_command


def main():
    print(f"COMMAND LINE INTERFACE\nYour Personal Assistant\n" + "=" * 23)
    print("If you wont to read reference to Personal Assistant,\nEnter <<help>> or <<reference>>")
    try:
        with open('data.json', 'r') as json_file:
            note_list = json.load(json_file)
            last_id = note_list[-1]['id']
            NoteRecord.counter = last_id
    except FileNotFoundError:
        note_list = []
    try:
        with open('data_test.bin', 'rb') as f:
            address_book = pickle.load(f)
    except FileNotFoundError:
        address_book = AddressBook()

    while True:
        try:
            command = input("Enter your command\n>>").lower()
            sep_command = command.split(" ")
            if sep_command[0] == "add" and sep_command[1] == "contact":
                address_book.add_record(Record(sep_command[2].title(),
                                               sep_command[3],
                                               sep_command[4] if len(sep_command) > 4 else '-',
                                               sep_command[5] if len(sep_command) > 5 else '-',
                                               sep_command[6:] if len(sep_command) > 6 else '-'))

            elif sep_command[0] == "add" and sep_command[1] == "note":
                title_ind = sep_command.index('-title') if '-title' in sep_command else None
                tag_index = sep_command.index('-tag') if '-tag' in sep_command else None
                if title_ind:
                    NoteRecord.counter += 1
                    main_note = NoteRecord(
                        ' '.join(sep_command[2:title_ind]), sep_command[tag_index + 1:] if tag_index else None,
                        ' '.join(sep_command[title_ind + 1: tag_index]) if tag_index else
                        ' '.join(sep_command[title_ind + 1:])
                    )
                    note_list.append(main_note.record)
                else:
                    print("You need to enter title!\n"
                          "Example: add note [your note] -title [title for your note] -tag(optional)\n")

            elif sep_command[0] == "add" and sep_command[1] == "tag":
                title_index = sep_command.index('-title') if '-title' in sep_command else None
                if not title_index:
                    print("I can't identify which note you mean!\nEnter title of it, please!\n"
                          "Example: add tag [tag] -title [title]")
                    continue
                for note in note_list:
                    if note['title'] == ' '.join(sep_command[title_index + 1:]):
                        working_note = note_list[note_list.index(note)]
                        if note['tag']:
                            working_note['tag'].extend(sep_command[2:title_index])
                        else:
                            working_note['tag'] = sep_command[2:title_index]

            elif sep_command[0] == "show" and sep_command[1] == "contact":
                address_book.find_contact(sep_command[2].title())

            elif sep_command[0] == "show" and sep_command[1] == "birthday":
                print(address_book.days_to_birthday(int(sep_command[2])))

            elif sep_command[0] == "show" and sep_command[1] == "all":
                address_book.__str__()

            elif sep_command[0] == "show" and sep_command[1] == "notes":
                print(f"Total notes: {NoteRecord.counter}")
                if not note_list:
                    print("List with notes is empty!")
                for note in note_list:
                    print(f"Title: {note['title']}\nNote: {note['note']}\nTags: {note['tag']}\n")

            elif sep_command[0] == "edit" and sep_command[1] == "contact":
                address_book.edit_contact(sep_command[2].title())

            elif sep_command[0] == "edit" and sep_command[1] == "note":
                change_index = sep_command.index('-edit') if '-edit' in sep_command else None
                if not change_index:
                    print("You didn't write text to change! Try again!\n"
                          "Example: edit note [title] -edit [new text]\n")
                count = 0
                for note in note_list:
                    count += 1
                    if change_index:
                        if note['title'] == ' '.join(sep_command[2:change_index]):
                            note['note'] = ' '.join(sep_command[change_index + 1:])
                            break
                    else:
                        ratio_of_coincidence = fuzz.WRatio(note['title'], ' '.join(sep_command[2:]))
                        if ratio_of_coincidence > 50:
                            print(f"Maybe you mean note with title {note['title']}? Try again!\n")
                        elif count == len(note_list) and ratio_of_coincidence < 20:
                            print(f"Note with this title {note['title']}!Try again!\n")

            elif sep_command[0] == "search" and sep_command[1] == "tags":
                founded_notes = NoteRecord.tag_search(note_list, sep_command[2])
                for item in founded_notes:
                    print(f"{item}")

            elif sep_command[0] == "search" and sep_command[1] == "note":
                for note in note_list:
                    rat_of_string = fuzz.WRatio(note['note'], ' '.join(sep_command[2:]))
                    if rat_of_string > 50:
                        print(f"Title: {note['title']}\nNote: {note['note']}")

            elif sep_command[0] == "sort" and sep_command[1] == "folders":
                sort_folder_command(sep_command[2:])
                print("Your folder just has been sorted!")

            elif sep_command[0] == "delete" and sep_command[1] == "contact":
                address_book.del_contact(sep_command[2].title())

            elif sep_command[0] == "delete" and sep_command[1] == "note":
                count = 0
                for note in note_list:
                    count += 1
                    if note['title'] == ' '.join(sep_command[2:]):
                        note_index = note_list.index(note)
                        note_list.pop(note_index)
                        NoteRecord.counter -= 1
                        break
                    else:
                        ratio_of_coincidence = fuzz.WRatio(note['title'], ' '.join(sep_command[2:]))
                        if ratio_of_coincidence > 50:
                            print(f"Maybe you mean note with title - {note['title']}?Try again!\n")
                        elif count == len(note_list) and ratio_of_coincidence < 20:
                            print("Does not exist! Try again!\n")

            elif command == "help" or command == "reference":
                help_command()

            elif command in ["good bye", "close", "exit"]:
                with open('data_test.bin', 'wb') as f:
                    pickle.dump(address_book, f)
                print("Good bye!\nHope see you soon!")
                if note_list:
                    NoteRecord().note_serialize(note_list)
                break

            else:
                command_dict = {1: "add contact", 2: "add note", 3: "add tag", 4: "show contact",
                                5: "show birthday", 6: "show all", 7: "show notes", 8: "edit contact",
                                9: "edit note", 10: "search tags", 11: "search note", 12: "sort folders",
                                13: "delete contact", 14: "delete note", 15: "help", 16: "reference",
                                17: "close", 18: "exit", 19: "good bye"}
                for value in command_dict.values():
                    ratio = int(difflib.SequenceMatcher(None, command, value).ratio() * 100)
                    if ratio > 50:
                        fixed_string = value[0] + value[1:]
                        print(f"You entered unknown command <<{command}>>. Maybe it`s <<{fixed_string}>>? Try again.")
                    elif ratio < 50:
                        continue

        except IndexError:
            print("Wrong input! Entered information is not enough for operation!")
        except KeyError:
            print("Wrong input! Check entered information!")


def help_command():
    """
    =====================================================
                 CLI - Command Line Interface
                       Personal Assistant
    =====================================================
    Personal Assistant works with Address book, write,
    save Notes and sort files in folders.
    Personal Assistant has a commands:
    1. "add contact" - for add name, address, contact
    information (phone, e-mail) and birthday to Address
    book write "add contact" then details and enter it;
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
    "edit contact" then name and enter it;
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
    print(help_command.__doc__)


if __name__ == "__main__":
    main()