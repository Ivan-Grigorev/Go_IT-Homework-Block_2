from flask import render_template, redirect, request, url_for

from app_folder import db, app
from app_folder.models import AddressBook


@app.route('/')
def main():
    return render_template('main_page.html')


@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        contact = AddressBook(name=request.form['name'].title(), phone=request.form['phone'],
                              email=request.form['email'], address=request.form['address'])
        db.session.add(contact)
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('add.html')


@app.route('/find', methods=['GET', 'POST'])
def find_contact():
    if request.method == 'GET':
        return render_template('find.html')
    return render_template('show_contact.html', items=db.session.query(AddressBook).filter_by(
        name=request.form.get('name').title()))


@app.route('/show', methods=['GET'])
def show_all():
    return render_template('show_all.html', items=db.session.query(AddressBook).all())


@app.route('/edit', methods=['GET', 'POST'])
def edit_contact():
    if request.method == 'POST':
        db.session.query(AddressBook).filter(AddressBook.name == request.form.get('edited_name').title()).update(
            {request.form.get('edited_data'): request.form.get('new_data')})
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('edit.html')


@app.route('/delete', methods=['GET', 'POST'])
def delete_contact():
    if request.method == 'POST':
        db.session.query(AddressBook).filter(AddressBook.name == request.form['deleted_name'].title()).delete()
        db.session.commit()
        return redirect(url_for('main'))
    return render_template('delete.html')


@app.route('/reference')
def help_command():
    return render_template('reference.html')


@app.route('/exit')
def exit_command():
    db.session.commit()
    db.session.close()
    return render_template('exit.html')
