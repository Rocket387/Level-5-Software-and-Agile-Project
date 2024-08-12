from flask import Blueprint, render_template, request, flash, jsonify, redirect,url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from datetime import datetime


#### routes/pages for web app ####

views = Blueprint('views',__name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note_content = request.form.get('eventBox')  # Assuming this is the note input field
        
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
    events_list = db.session.execute(db.select(Note).order_by(Note.date)).scalars()
    
    return render_template('home.html', user=current_user, eventsList=events_list)
@views.route('/delete-note', methods=['POST'])
def delete_note():
    #if user == Admin
    info = json.loads(request.data)
    noteId = info['noteId']
    info = Note.query.get(noteId)
    if info:
        if info.user_id == current_user.id:
            db.session.delete(info)
            db.session.commit()
    #else:
    # DO NOT SHOW DELETE
    return jsonify({})
