import React, { useState, useEffect } from 'react';
import { Button, Form, Table, Alert } from 'react-bootstrap';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { fetchChatbotInteractions } from '../api';


const ChatbotInteractions = ({ currentUser, currentUserRole }) => {
  const [interactions, setInteractions] = useState([]);
  const [searchParams, setSearchParams] = useState({
    userAlias: '',
    keyword: '',
    startDate: '',
    endDate: ''
  });
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  // Redirect non-admin users away
  useEffect(() => {
    if (currentUserRole !== 'Admin') {
      navigate('/');
    }
  }, [currentUserRole, navigate]);

  // Fetch interactions
  const fetchInteractions = async () => {
    try {
      const response = await fetchChatbotInteractions(searchParams);
      setInteractions(response.data.interactions || []);
      setMessage('');
    } catch (error) {
      console.error('Error fetching interactions:', error);
      setMessage('Error fetching interactions. Please try again.');
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setSearchParams((prev) => ({ ...prev, [name]: value }));
  };

  const handleSearch = (e) => {
    e.preventDefault();
    fetchInteractions();
  };

  return (
    <div style={{ margin: '20px' }}>
      <h2>Chatbot Interactions</h2>

      {message && <Alert variant="danger">{message}</Alert>}

      {/* Search Form */}
      <Form onSubmit={handleSearch} style={{ marginBottom: '20px' }}>
        <Form.Group controlId="userAlias">
          <Form.Label>User Alias</Form.Label>
          <Form.Control
            type="text"
            name="userAlias"
            value={searchParams.userAlias}
            onChange={handleInputChange}
            placeholder="Search by user alias"
          />
        </Form.Group>

        <Form.Group controlId="keyword">
          <Form.Label>Keyword</Form.Label>
          <Form.Control
            type="text"
            name="keyword"
            value={searchParams.keyword}
            onChange={handleInputChange}
            placeholder="Search by keyword"
          />
        </Form.Group>

        <Form.Group controlId="startDate">
          <Form.Label>Start Date</Form.Label>
          <Form.Control
            type="date"
            name="startDate"
            value={searchParams.startDate}
            onChange={handleInputChange}
          />
        </Form.Group>

        <Form.Group controlId="endDate">
          <Form.Label>End Date</Form.Label>
          <Form.Control
            type="date"
            name="endDate"
            value={searchParams.endDate}
            onChange={handleInputChange}
          />
        </Form.Group>

        <Button variant="primary" type="submit" style={{ marginTop: '10px' }}>
          Search
        </Button>
      </Form>

      {/* Display Interactions */}
      <Table striped bordered hover>
        <thead>
          <tr>
            <th>User Alias</th>
            <th>Message</th>
            <th>Response</th>
            <th>Date</th>
          </tr>
        </thead>
        <tbody>
          {interactions.length === 0 ? (
            <tr>
              <td colSpan="4">No interactions found.</td>
            </tr>
          ) : (
            interactions.map((interaction) => (
              <tr key={interaction.id}>
                <td>{interaction.userAlias || 'Anonymous'}</td>
                <td>{interaction.message}</td>
                <td>{interaction.response}</td>
                <td>{new Date(interaction.timestamp).toLocaleString()}</td>
              </tr>
            ))
          )}
        </tbody>
      </Table>
    </div>
  );
};

export default ChatbotInteractions;
