import React, { useState } from 'react';
import { Button, Form, Alert } from 'react-bootstrap';
import axios from 'axios';
import { Link } from 'react-router-dom';
import api from '../api'; 

const Login = ({ onLogin }) => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleInputChange = (e) => {
  const { name, value } = e.target;

 
  if (name === 'email') {
    const invalidPattern = /[<>/"'`;[\]]/;
    if (invalidPattern.test(value)) {
      setError('Invalid characters detected in email. Please remove any of the following: <, >, /, ", \', `, ;, [, ]');
    } else {
      setError(''); 
    }
  }

  setFormData((prevData) => ({ ...prevData, [name]: value }));
};

  const handleLogin = async (e) => {
  e.preventDefault();
  setError('');
  setSuccess('');

  try {
    const response = await api.post('/api/auth/login', formData);
    setSuccess(response.data.message);
    onLogin(formData.email);
  } catch (err) {
    console.error('Error during login', err);
    setError(err.response?.data?.error || 'Failed to login. Please try again.');
  }
};

  return (
    <div className="login-container">
      {error && <Alert variant="danger">{error}</Alert>}
      {success && <Alert variant="success">{success}</Alert>}

      <Form onSubmit={handleLogin}>
        <Form.Group controlId="formEmail">
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

        <Form.Group controlId="formPassword">
          <Form.Label>Password</Form.Label>
          <Form.Control
            type="password"
            placeholder="Password"
            name="password"
            value={formData.password}
            onChange={handleInputChange}
            required
          />
        </Form.Group>

        <Button variant="primary" type="submit" style={{ marginTop: '20px' }}>
          Login
        </Button>
      </Form>

      <p className="mt-3">
        Don't have an account? <Link to="/signup">Sign up</Link>
      </p>
    </div>
  );
};

export default Login;
