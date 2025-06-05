import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import handleLogout from './logout'; // Adjust the import path as needed

const NavbarComponent = () => {
  const navigate = useNavigate();

  const onNavigate = (route) => {
    console.log('Navigating to:', route);
    switch(route) {
      case 'NoteKeeper':
        navigate('/notekeeper');
        break;
      default:
        console.error('Invalid route:', route);
    }
  };

  return (
    <Navbar className="nav-back custom-navbar" expand="lg">
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto">
          <Nav.Link className="custom-nav-link" onClick={handleLogout}>Logout</Nav.Link>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
};

export default NavbarComponent;
