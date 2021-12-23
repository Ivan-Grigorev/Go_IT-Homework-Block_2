from collections import UserDict
from datetime import timedelta, date, datetime
import re
import time


class Name:
    def __init__(self, name):
        self.__name = None
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name: str):
        if len(name) > 0:
            self.__name = name
        else:
            print("Incorrect name!")

    def __str__(self):
        return f"{self.__name}"


class Phone:
    def __init__(self, phone):
        self.__phone = None
        self.phone = phone

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, phone: str):
        if phone == '-':
            self.__phone = phone
        else:
            if re.search("(^\+?(38)?0(44|67|68|96|97|98|50|66|95|99|63|73|93|89|94)\d{7}$)", re.sub(r'\D', "", phone)):
                if len(re.sub(r'\D', "", phone)) == 12:
                    self.__phone = '+' + re.sub(r'\D', "", phone)
                else:
                    self.__phone = '+38' + re.sub(r'\D', "", phone)
            else:
                self.__phone = '-'
                print("The phone is not saved because it has an incorrect format\n"
                      "Try to edit like the example: +38(0**)*******")

    def __str__(self):
        return f"{self.__phone}"


class Email:
    def __init__(self, email):
        self.__email = None
        self.email = email

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        if email == '-':
            self.__email = email
        else:
            if re.search("^[\w\.-]+@[\w\.-]+(\.[\w]+)+", email):
                self.__email = email
            else:
                self.__email = '-'
                print("The email is not saved because it has an incorrect format\n"
                      "Try to edit like the example: *****@***.***")

    def __str__(self):
        return f"{self.__email}"


class Birthday:
    def __init__(self, birthday):
        self.__birthday = None
        self.birthday = birthday

    @property
    def birthday(self):
        return self.__birthday

    @birthday.setter
    def birthday(self, birthday):
        if birthday == '-':
            self.__birthday = birthday
        else:
            try:
                if time.strptime(birthday, '%d/%m/%Y'):
                    self.__birthday = birthday
            except ValueError:
                self.__birthday = '-'
                print("The date is not saved because it has an incorrect format\n"
                      "Try to edit like the example: DD/MM/YYYY")

    def __str__(self):
        return f"{self.__birthday}"


class Address:
    def __init__(self, address):
        self.address = address
        self.__address = address

    def __str__(self):
        return f"{','.join(self.__address).title()}"


class Record:
    def __init__(self, name, phone, email, birthday, address):
        self.name = Name(name)
        self.phone = Phone(phone)
        self.email = Email(email)
        self.birthday = Birthday(birthday)
        self.address = Address(address)

    def __str__(self):
        return f"{self.phone},{self.email},{self.birthday},{self.address}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.__str__()] = record

    def find_contact(self, name):
        for key, value in self.data.items():
            if str(name) == str(key):
                print(f"{key}: {value}")

    def del_contact(self, name):
        try:
            question = input("Are you sure?: Y/N\n>>").lower()
            if question == 'y':
                self.data.pop(name)
                print(f"{name} was successfully deleted.")
        except KeyError:
            print("This contact does not exist in Address Book")

    def edit_contact(self, name):
        print(self.data[name])
        edit_option = input("Enter an editable option (phone, email, birthday or address)"
                            " and information to change: ").lower()
        sep_edit_option = edit_option.split(' ')
        data = str(self.data[name]).split(',')
        if sep_edit_option[0] == 'phone':
            data[0] = sep_edit_option[1]
            AddressBook.add_record(self, Record(name, data[0], data[1], data[2], data[3:]))
        if sep_edit_option[0] == 'email':
            data[1] = sep_edit_option[1]
            AddressBook.add_record(self, Record(name, data[0], data[1], data[2], data[3:]))
        if sep_edit_option[0] == 'birthday':
            data[2] = sep_edit_option[1]
            AddressBook.add_record(self, Record(name, data[0], data[1], data[2], data[3:]))
        if sep_edit_option[0] == 'address':
            data[3] = sep_edit_option[1:]
            AddressBook.add_record(self, Record(name, data[0], data[1], data[2], data[3:]))

    def days_to_birthday(self, number_days):
        end_date = date.today() + timedelta(days=number_days)
        first_list = []
        try:
            for key, val in self.data.items():
                result = re.search(r"\d{1,2}\/\d{1,2}\/\d{4}", str(val)).group()
                if datetime.strptime(result, "%d/%m/%Y").month == end_date.month \
                        and datetime.strptime(result, "%d/%m/%Y").day == end_date.day:
                    first_list.append({str(key): str(val)})
        except AttributeError:
            pass
        return first_list

    def __str__(self):
        print(f"Total contacts in Address Book: {len(self.data)}")
        for key, val in self.data.items():
            print(f"{str(key)}:{str(val)}".removesuffix(','))
