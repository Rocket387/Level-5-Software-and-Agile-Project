import axios from 'axios';

function getUrl() {
  if (process.env.CODESPACES === "true") {
    return `https://${process.env.CODESPACE_NAME}-5300.app.github.dev`;
  } else {
    return `http://localhost:8080`;  // Your backend Flask port
  }
}

const baseURL = getUrl();

const api = axios.create({
  baseURL,
  withCredentials: true,  // Helps with session-based login/logout
});

// Auth
export const signup = (payload) =>
  api.post('/api/auth/signup', payload, {
    headers: { 'Content-Type': 'application/json' }
  });

export const login = (payload) =>
  api.post('/api/auth/login', payload, {
    headers: { 'Content-Type': 'application/json' }
  });

export const logout = () =>
  api.post('/api/auth/logout', {}, {
    headers: { 'Content-Type': 'application/json' },
    withCredentials: true
  });

// Notes
export const notekeeperCreate = (payload) =>
  api.post('/api/notes', payload, {
    headers: { 'Content-Type': 'application/json' }
  });

export const notekeeperFetch = () =>
  api.get('/api/notes', {
    withCredentials: true  
  });

export const notekeeperUpdate = (noteId, payload) =>
  api.put(`/api/notes/${noteId}`, payload, {
    headers: { 'Content-Type': 'application/json' }
  });

export const notekeeperDelete = (noteId) =>
  api.delete(`/api/notes/${noteId}`);

// Chatbot
export const chatbotSend = (user_input) =>
  api.post('/api/chat', { user_input }, {
    headers: { 'Content-Type': 'application/json' }
  });

export const fetchChatbotInteractions = (params) =>
  api.get('/api/admin/chatbot-interactions', { params });

export default api;
