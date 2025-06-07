import React, { useState } from 'react';
import { Button, Form, Alert } from 'react-bootstrap';
import axios from 'axios';
import { Link } from 'react-router-dom';
import api from '../api';

const Signup = ({ onSignup }) => {
  const [formData, setFormData] = useState({
    email: '',
    alias: '',
    password1: '',
    password2: ''
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleInputChange = (e) => {
  const { name, value } = e.target;

 
  if (name === 'email' || name === 'alias') {
    const invalidPattern = /[<>/"'`;[\]]/;
    if (invalidPattern.test(value)) {
      setError('Invalid characters detected in email. Please remove any of the following: <, >, /, ", \', `, ;, [, ]');
    } else {
      setError(''); 
    }
  }

  setFormData((prevData) => ({ ...prevData, [name]: value }));
};

  const handleSignup = async (e) => {
  e.preventDefault();
  setError('');
  setSuccess('');


  try {
    const response = await api.post('/api/auth/signup', formData);
    setSuccess(response.data.message);
    onSignup(formData.email);
  } catch (err) {
    console.error('Error during signup', err);
    setError(err.response?.data?.error || 'Failed to signup. Please try again.');
  }
};

  return (
    <div>
      {error && <Alert variant="danger">{error}</Alert>}
      {success && <Alert variant="success">{success}</Alert>}

      <Form onSubmit={handleSignup}>
        <Form.Group controlId="formBasicEmail">
          <Form.Label>Email</Form.Label>
          <Form.Control
            type="email"
            placeholder="Enter email"
            name="email"
            value={formData.email}
            onChange={handleInputChange}
            required
          />
        </Form.Group>

        <Form.Group controlId="formBasicAlias">
          <Form.Label>Alias</Form.Label>
          <Form.Control
            type="text"
            placeholder="Enter alias"
            name="alias"
            value={formData.alias}
            onChange={handleInputChange}
            required
          />
        </Form.Group>

        <Form.Group controlId="formBasicPassword1">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Password"
            name="password1"
            value={formData.password1}
            onChange={handleInputChange}
            required
          />
        </Form.Group>

        <Form.Group controlId="formBasicPassword2">
          <Form.Label>Confirm Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Confirm Password"
            name="password2"
            value={formData.password2}
            onChange={handleInputChange}
            required
          />
        </Form.Group>

        <Button variant="primary" type="submit" style={{ marginTop: '20px' }}>
          Signup
        </Button>
      </Form>

      <p className="mt-3">
        Already have an account? <Link to="/login">Login</Link>
      </p>
    </div>
  );
};

export default Signup;
