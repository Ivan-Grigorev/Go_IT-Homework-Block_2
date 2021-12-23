import difflib
import re

from pymongo import MongoClient


client = MongoClient(
        'mongodb+srv://Ivan_Grigorev:mongo_cloud_28.09_ig@cluster0.nzrg5.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
    )

db = client.module_10_hw


def main():
    print(f"COMMAND LINE INTERFACE\nYour Personal Assistant\n" + "=" * 23)
    print("If you wont to read reference to Personal Assistant,\nEnter <<help>> or <<reference>>")

    while True:
        try:
            command = input("Enter your command\n>>").lower()
            sep_command = command.split(' ')
            if sep_command[0] == 'add' and sep_command[1] == 'contact':
                name = input("Enter name, please\n>>").title()
                if len(name) == 0:
                    raise IndexError
                phone = input("Enter phone, please\n(To skip, press 'Enter')\n>>")
                if len(phone) == 0:
                    phone += '-'
                else:
                    if re.search('(^\+?(38)?0(44|67|68|96|97|98|50|66|95|99|63|73|93|89|94)\d{7}$)',
                                 re.sub(r'\D', '', phone)):
                        if len(re.sub(r'\D', '', phone)) == 12:
                            phone = '+' + re.sub(r'\D', '', phone)
                        else:
                            phone = '+38' + re.sub(r'\D', '', phone)
                    else:
                        print("The phone is not saved because it has incorrect format.\n"
                              "Try to edit like the example: +38(***)*******")
                        raise TypeError
                email = input("Enter e-mail, please\n(To skip, press 'Enter')\n>>")
                if len(email) == 0:
                    email += '-'
                else:
                    if re.search('^[\w\.-]+@[\w\.-]+(\.[\w]+)+', email):
                        email = email
                    else:
                        print("The email is not saved because it has an incorrect format.\n"
                              "Try to edit like the example: *****@***.***")
                        raise TypeError
                address = [input("Enter address, please\n(To skip, press 'Enter')\n>>")]
                if len(address) == 0:
                    address += '-'
                db.address_book.insert_one(
                    {'name': name, 'phone': phone, 'e-mail': email, 'address': address}
                )

            elif sep_command[0] == 'show' and sep_command[1] == 'contact':
                address_book_data = db.address_book.find_one({'name': sep_command[2].title()})
                print(address_book_data)

            elif sep_command[0] == 'show' and sep_command[1] == 'all':
                address_book_data = db.address_book.find({})
                for row in address_book_data:
                    print(row)

            elif sep_command[0] == 'edit' and sep_command[1] == 'contact':
                edited_name = input("Enter name, please\n>>").title()
                edited_data = input("Enter what you want to edit, please\n>>")
                new_data = input(f"Enter new {edited_data}, please\n>>")
                db.address_book.update_one({'name': edited_name}, {'$set': {edited_data: new_data}})

            elif sep_command[0] == 'delete' and sep_command[1] == 'contact':
                deleted_name = input("Enter name to delete, please\n>>").title()
                answer = input("Are you sure? Y/N\n>>")
                if answer.title() == 'Y':
                    db.address_book.delete_one({'name': deleted_name})
                else:
                    continue

            elif command == 'help' or command == 'reference':
                help_command()

            elif command in ['goodbye', 'close', 'exit']:
                print("Goodbye!\nHope see you soon!")
                break

            else:
                command_dict = {1: 'add contact', 2: 'show contact', 3: 'show all',
                                4: 'edit contact', 5: 'delete contact', 6: 'help',
                                7: 'reference', 8: 'close', 9: 'exit', 10: 'goodbye'}
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
        except TypeError:
            print("Wrong input! Check entered information! ")


def help_command():
    """
    =====================================================
                 CLI - Command Line Interface
                       Personal Assistant
    =====================================================
    Personal Assistant works with Address.
    Personal Assistant has a commands:
    1. "add contact" - for add name, contact information
    (phone, e-mail) and address to Address book write
    "add contact" and enter command then Assistant ask
    you details enter it;
    2. "show contact" - for get all contact information
    write "show contact" then name and enter it;
    3. "show all" - for show all contacts in Address book
    write "show all" and enter command;
    4. "edit contact" - for edit contact information write
    "edit contact" and enter command then Assistant ask
    details enter it;
    5. "delete contact" - for delete name and contact
    information in Address book write "delete contact" and
    then Assistant ask name enter it;
    6. "help", "reference" - for ask reference how to
    use Personal Assistant write "help" or "reference"
    and enter the command;
    7. "close", "exit", "goodbye" - for finish work with
    Personal Assistant, write one of "close", "exit" or
    "goodbye" and enter command then you will exit from
    Command Line Interface.

    Pleasant use!
    """
    print(help_command.__doc__)


if __name__ == "__main__":
    main()

