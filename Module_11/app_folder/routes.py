from flask import render_template, redirect, request, url_for, flash

from Module_11.app_folder import db, app
from forms import AddContactForm
from models import AddressBook


@app.route('/', methods=['GET', 'POST'])
def main():
    return render_template('start_page.html')


@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    form = AddContactForm()
    if form.validate_on_submit():
        contact = AddressBook(name=form.name.data, phone=form.phone.data,
                              email=form.email.data, address=form.address.data)
        db.session.add(contact)
        db.session.commit()
        flash("Successfully added contact!")
        return redirect(url_for('main'))
    return render_template('add.html')


@app.route('/find', methods=['GET', 'Post'])
def find_contact():
    if request.method == 'POST':
        name = request.form.get('name').title()
        return render_template('show.html', items=db.session.query(AddressBook).filter_by(name=name))
    return render_template('find.html')


@app.route('/show', methods=['GET', 'POST'])
def show_all():
    return render_template('show.html', items=db.session.query(AddressBook).all())


@app.route('/edit', methods=['GET', 'POST'])
def edit_contact():
    if request.method == 'POST':
        edited_name = request.form.get('edited_name').title()
        edited_data = request.form.get('edited_data')
        new_data = request.form.get('new_data')
        db.session.query(AddressBook).filter(AddressBook.name == edited_name).update({edited_data: new_data})
        return redirect(url_for('main'))
    return render_template('edit.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete_contact():
    if request.method == 'POST':
        deleted_name = request.form.get('deleted_name').title()
        db.session.query(AddressBook).filter(AddressBook.name == deleted_name).delete()
        return redirect(url_for('main'))
    return render_template('delete.html')


@app.route('/reference', methods=['GET', 'POST'])
def help_command():
    return render_template('reference.html')


@app.route('/exit', methods=['GET', 'POST'])
def exit_command():
    db.session.commit()
    db.session.close()
    return render_template('exit.html')
