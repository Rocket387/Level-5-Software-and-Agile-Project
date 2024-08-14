from flask import Blueprint, render_template, request, flash, jsonify, redirect,url_for
from flask_login import login_required, current_user
from .models import Note, User
from . import db
import json
from datetime import datetime


#### routes/pages for web app ####

views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note_content = request.form.get('eventBox')  # Note input field
        
        if len(note_content) < 1:
            flash('Note is too short', category='error')
        else:
            # Create a new Note object with the current datetime and the note content
            new_note = Note(info=note_content, date=datetime.now(), user_id=current_user.id)
            
            # Add and commit the new note to the database
            db.session.add(new_note)
            db.session.commit()
            flash('Note added', category='success')
        
        # Redirect to avoid form resubmission issues
        return redirect(url_for('views.home'))

    # Query all notes and order by date for the homepage
    events_list = db.session.query(Note).join(User).order_by(Note.date).all()
    
    return render_template('home.html', user=current_user, eventsList=events_list)

@views.route('/edit-note/<int:note_id>', methods=['POST'])
@login_required
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)

    #Ensure current user is owner of the note
    if note.user_id != current_user.id:
        flash('You do not have permission to edit this note!', category='error')
        return redirect(url_for('views.home'))
    
    #update the note with the new info from the form
    updated_info = request.form.get('updated_info')
    if updated_info and len(updated_info) > 0:
        note.info = updated_info
        note.date = datetime.now()
        db.session.commit()
        flash('Note successfully updated!', category='success')
    else:
        flash('Note content cannot be empty', category='error')
    
    return redirect(url_for('views.home'))

@views.route('/delete-note/<int:note_id>')
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)

    if current_user.role.roleName != 'Admin':
        flash('You do not have permission to delete this note.', category='error')
        return redirect(url_for('views.home'))

    db.session.delete(note)
    db.session.commit()
    flash('Note deleted successfully.', category='success')

    return redirect(url_for('views.home'))
