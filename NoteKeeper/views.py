from flask import Blueprint, render_template, request, flash, jsonify, redirect,url_for
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json
from datetime import datetime


#### routes/pages for web app ####

#blueprint organizes related views and code
views = Blueprint('views',__name__)

#home page fetches, adds and edits data from the database
@views.route('/', methods=['GET', 'POST'])
#login is required for user to access this page
@login_required
def home():
    if request.method == 'POST':
        note_content = request.form.get('eventBox')  #note input field
        
        #validation rule ensures note is not just one letter
        if len(note_content) < 1:
            flash('Note is too short', category='error')
        else:
            #new Note created with the current date and the note content
            new_note = Note(info=note_content, date=datetime.now(), user_id=current_user.id)
            
            #adds new note to the database
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
        
        #redirect to prevent resubmission issues
        return redirect(url_for('views.home'))

    #queries all notes and orders them by date for the homepage
    events_list = db.session.query(Note).join(User).order_by(Note.date).all()
   
   #redirect to prevent resubmission issues
    return render_template('home.html', user=current_user, eventsList=events_list)

#function permits users to edit their notes, base path and variable for note_id to identify which note to edit
@views.route('/edit-note/<int:note_id>', methods=['POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)

    #checks current user owns the note otherwise they cannot edit it
    if note.user_id != current_user.id:
        flash('You do not have permission to edit this note!', category='error')
        #redirect to prevent resubmission issues
        return redirect(url_for('views.home'))
    
    #if user owns the note checks and edited information contains at least one letter note will be updated
    updated_info = request.form.get('updated_info')
    if updated_info and len(updated_info) > 0:
        note.info = updated_info
        note.date = datetime.now()
        db.session.commit()
        flash('Note successfully updated!', category='success')
    else:
        #lets the user know edits must be at least 1 character change
        flash('Note content cannot be empty', category='error')
    
    #redirect to prevent resubmission issues
    return redirect(url_for('views.home'))

#function for Admin users to delete notes
@views.route('/delete-note/<int:note_id>')
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    #checks users roleName is equivalent to Admin
    if current_user.role.roleName != 'Admin':
        flash('You do not have permission to delete this note.', category='error')
        return redirect(url_for('views.home'))

    #if Admin user note is deleted when delete button is clicked
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted successfully.', category='success')

    #redirect to prevent resubmission issues
    return redirect(url_for('views.home'))
