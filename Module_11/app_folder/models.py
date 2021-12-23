from Module_11.app_folder import db


class AddressBook(db.Model):
    __tablename__ = 'address_book'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    phone = db.Column(db.String)
    email = db.Column(db.String)
    address = db.Column(db.String)

    def __init__(self, name, phone, email, address):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address

    def __repr__(self):
        return f"{self.name},{self.phone},{self.email},{self.address}"


db.create_all()
