import difflib
import json
import pickle
from fuzzywuzzy import fuzz

from address_book import AddressBook, Record
from notes import NoteRecord
from sort_folder import sort_folder_command


def main():
    global get_address_book, get_notes
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
                name = input("Enter name, please\n>>").title()
                phone = input("Enter phone, please\n(To skip, press 'Enter')\n>>")
                if len(phone) == 0:
                    phone += '-'
                email = input("Enter e-mail, please\n(To skip, press 'Enter')\n>>")
                if len(email) == 0:
                    email += '-'
                birthday = input("Enter birthday, please\n(To skip, press 'Enter')\n>>")
                if len(birthday) == 0:
                    birthday += '-'
                address = input("Enter address, please\n(To skip, press 'Enter')\n>>")
                if len(address) == 0:
                    address += '-'
                address_book.add_record(Record(name, phone, email, birthday, address))

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
                from get_info import GetAddressBook
                get_address_book = GetAddressBook()
                get_address_book.find_info()

            elif sep_command[0] == "show" and sep_command[1] == "birthday":
                print(address_book.days_to_birthday(int(sep_command[2])))

            elif sep_command[0] == "show" and sep_command[1] == "all":
                from get_info import GetAddressBook
                get_address_book = GetAddressBook()
                get_address_book.show_info()

            elif sep_command[0] == "show" and sep_command[1] == "notes":
                from get_info import GetNotes
                get_notes = GetNotes()
                get_notes.show_info()

            elif sep_command[0] == "edit" and sep_command[1] == "contact":
                name = input("Enter name, please\n>>")
                address_book.edit_contact(name.title())

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
                from get_info import GetNotes
                get_notes.find_info()

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
                from get_info import GetHelpInfo
                get_help_info = GetHelpInfo()
                get_help_info.show_info()

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


if __name__ == "__main__":
    main()

