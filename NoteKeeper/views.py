from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from notekeeper.models import Note, User, ChatbotInteraction
from notekeeper.extensions import db
from datetime import datetime

views = Blueprint('views', __name__)

# GET all notes
@views.route('/api/notes', methods=['GET'])
@login_required
def get_notes():
    all_notes = Note.query.order_by(Note.date.desc()).all()

    notes_list = []
    for note in all_notes:
        notes_list.append({
            'id'       : note.id,
            'info'     : note.info,
            'date'     : note.date.strftime('%d-%M-%Y'),
            'userAlias': note.user.alias,   # relationship attribute
            'canEdit'  : note.user_id == current_user.id
                           or current_user.role.roleName == 'Admin',
            'canDelete': note.user_id == current_user.id
                           or current_user.role.roleName == 'Admin'
        })

    return jsonify({'notes': notes_list}), 200

# POST a new note
@views.route('/api/notes', methods=['POST'])
@login_required
def create_note():
    data = request.get_json()
    description = data.get('description')
    date_str = data.get('date')
    
    if not description or len(description) < 1:
        return jsonify({'error': 'Note is too short'}), 400

    try:
        date = datetime.fromisoformat(date_str.rstrip('Z')) if date_str else datetime.utcnow()
    except Exception:
        date = datetime.utcnow()
        
    new_note = Note(info=description, date=date, user_id=current_user.id, role_id=current_user.role_id)
    db.session.add(new_note)
    db.session.commit()
    return jsonify({'message': 'Note added successfully'}), 201

# PUT (edit) an existing note
@views.route('/api/notes/<int:note_id>', methods=['PUT'])
@login_required
def update_note(note_id):
    note = Note.query.get_or_404(note_id)

    # Only owner or admin can edit
    if note.user_id != current_user.id and current_user.role.roleName != 'Admin':
        return jsonify({'error': 'You do not have permission to edit this note.'}), 403

    data = request.get_json()
    new_info = data.get('description')
    if not new_info or len(new_info) < 1:
        return jsonify({'error': 'Note content cannot be empty'}), 400

    note.info = new_info
    note.date = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Note updated successfully'}), 200

# DELETE a note (Admin or owner only)
@views.route('/api/notes/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    
    if current_user.role.roleName != 'Admin' and note.user_id != current_user.id:
        return jsonify({'error': 'You do not have permission to delete this note.'}), 403

    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': 'Note deleted successfully'}), 200

@views.route('/api/admin/chatbot-interactions', methods=['GET'])
@login_required
def search_chatbot_interactions():
    if not current_user.has_role('Admin'):
        return jsonify({'error': 'You do not have permission.'}), 403

    user_alias = request.args.get('userAlias')
    keyword = request.args.get('keyword')
    start_date = request.args.get('startDate')
    end_date = request.args.get('endDate')

    query = ChatbotInteraction.query.join(User, isouter=True)

    if user_alias:
        query = query.filter(User.alias.ilike(f"%{user_alias}%"))
    if keyword:
        query = query.filter(
            (ChatbotInteraction.message.ilike(f"%{keyword}%")) |
            (ChatbotInteraction.response.ilike(f"%{keyword}%"))
        )
    if start_date:
        query = query.filter(ChatbotInteraction.timestamp >= start_date)
    if end_date:
        query = query.filter(ChatbotInteraction.timestamp <= end_date)

    interactions = query.order_by(ChatbotInteraction.timestamp.desc()).all()

    interactions_data = [{
        'id': i.id,
        'message': i.message,
        'response': i.response,
        'timestamp': i.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'userAlias': i.user.alias if i.user else 'Anonymous'
    } for i in interactions]

    return jsonify({'interactions': interactions_data}), 200