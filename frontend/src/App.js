import React from 'react';
import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import NavbarComponent from './components/navbar';
import NoteKeeper from './components/notekeeper';
import Footer from './components/footer';
import Login from './components/login';
import Signup from './components/signup';
import logo from './img/pv.png'; 
import ChatBot from './components/chatbot';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [currentUser, setCurrentUser] = useState(''); 

  const handleLogout = () => {
    setIsLoggedIn(false); 
    setCurrentUser(''); 
  };

  const handleLogin = (username) => { 
    setIsLoggedIn(true);
    setCurrentUser(username);
  };

  return (
    <div className="App">
      <Router>
        <div className="appTitle">
          <h1>Prime Video Daily StandUp Notes & ChatBot assistant</h1>
          <img src={logo} alt="Prime Video Logo" id="appLogo" />
        </div>

        {isLoggedIn && <NavbarComponent onLogout={handleLogout} />}

        <div className="componentContainer">
          <Routes>
            <Route path="/login" element={isLoggedIn ? <Navigate to="/" /> : <Login onLogin={handleLogin} />} />
            <Route path="/signup" element={isLoggedIn ? <Navigate to="/" /> : <Signup onSignup={(username) => {
              setIsLoggedIn(true);
              setCurrentUser(username);
            }} />} />
            <Route path="/" element={isLoggedIn ? <NoteKeeper currentUser={currentUser} /> : <Navigate to="/login" />} />
          </Routes>
        </div>
        <Footer />
        <ChatBot />
      </Router>
    </div>
  );
}

export default App;