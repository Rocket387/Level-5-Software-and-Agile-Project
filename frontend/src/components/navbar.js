import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import handleLogout from './logout';

const NavbarComponent = ({ onLogout }) => {
  const navigate = useNavigate();

  const onClickLogout = async () => {
    await handleLogout(navigate); 
    if (onLogout) {
      onLogout();
    }
  };

  return (
    <Navbar className="nav-back custom-navbar" expand="lg">
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link className="custom-nav-link" onClick={onClickLogout}>Logout</Nav.Link>
          <Nav.Link className="custom-nav-link" onClick={() => navigate('/chatbot-interactions')}>Chatbot Logs</Nav.Link>
          <Nav.Link className="custom-nav-link" onClick={() => navigate('/api/notes')}>NoteKeeper</Nav.Link>

        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default NavbarComponent;
