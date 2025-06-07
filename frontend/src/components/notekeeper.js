import React, { useEffect, useState } from 'react';
import { Button, Form, Table, Modal } from 'react-bootstrap';
import axios from 'axios';
import 'react-datepicker/dist/react-datepicker.css';
import {
  notekeeperCreate,
  notekeeperFetch,
  notekeeperUpdate,
  notekeeperDelete
} from '../api';

const NoteKeeper = ({ currentUser, currentUserRole }) => {
  const [notes, setNotes] = useState([]);
  const [newNote, setNewNote] = useState({ description: '', date: new Date() });
  const [message, setMessage] = useState('');
  const [editingNote, setEditingNote] = useState(null);

  // Fetch notes from backend
  const fetchNotes = async () => {
    try {
      const res = await notekeeperFetch();
      setNotes(res.data.notes || []);
    } catch (err) {
      console.error('Error fetching notes:', err);
    }
  };

  useEffect(() => {
    fetchNotes();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editingNote) {
        // Update note
        await axios.put(`/api/notes/${editingNote.id}`, { ...newNote });
        setMessage('Note updated successfully.');
        setEditingNote(null);
      } else {
        // Create note
        await notekeeperCreate({ ...newNote, username: currentUser });
        setMessage('Note added successfully.');
      }
      setNewNote({ description: '', date: new Date() });
      fetchNotes();
      setTimeout(() => setMessage(''), 2000);
    } catch (error) {
      console.error('Error submitting note:', error);
    }
  };

  const handleEdit = (note) => {
    setEditingNote(note);
    setNewNote({ description: note.info, date: new Date(note.date) });
  };

  const handleDelete = async (noteId) => {
  const confirmDelete = window.confirm('Are you sure you want to delete this note?');
  if (!confirmDelete) {
    return; // User canceled deletion
  }

  try {
    await notekeeperDelete(noteId);
    setMessage('Note deleted.');
    fetchNotes();
    setTimeout(() => setMessage(''), 2000);
  } catch (err) {
    console.error('Error deleting note:', err);
  }
};


  return (
    <div>
      <h3>Notes</h3>
      {message && <p style={{ color: 'green' }}>{message}</p>}
      <Table striped bordered hover style={{ marginTop: '10px' }}>
  <thead>
    <tr>
      <th>Alias</th>
      <th>Date</th>
      <th>Note</th>
      <th></th>
      <th></th> 
    </tr>
  </thead>
  <tbody>
    {notes.map((note) => {
      const isNoteOwner = note.userAlias === currentUser;
      const isAdmin = currentUserRole === 'Admin';
      return (
        <tr key={note.id}>
          <td>{note.userAlias}</td>
          <td>{note.date}</td>
          <td>{note.info}</td>
          <td>
            {(isNoteOwner || isAdmin) && (
              <Button variant="primary" size="sm" onClick={() => handleEdit(note)}>
                Edit
              </Button>
            )}
          </td>
          <td>
            {(isNoteOwner || isAdmin) && (
              <Button
                variant="danger"
                size="sm"
                onClick={() => handleDelete(note.id)}
              >
                Delete
              </Button>
            )}
          </td>
        </tr>
      );
    })}
  </tbody>
</Table>


      <Form onSubmit={handleSubmit} style={{ maxWidth: '400px', margin: 'auto' }}>
      

        <Form.Group controlId="description" style={{ marginBottom: '20px' }}>
          <Form.Label>Add Note:</Form.Label>
          <Form.Control
            as="textarea"
            rows={3}
            required
            value={newNote.description}
            onChange={(e) => setNewNote({ ...newNote, description: e.target.value })}
          />
        </Form.Group>

        <Button variant="success" type="submit">
          {editingNote ? 'Update Note' : 'Save Note'}
        </Button>
      </Form>
    </div>
  );
};

export default NoteKeeper;
