// logout.js
import axios from 'axios';
import { logout } from '../api';  

const handleLogout = async () => {
  try {
    
    const confirmLogout = window.confirm('Are you sure you want to log out?');
    if (!confirmLogout) {
      return; // User canceled logout
    }
    const response = await logout();
    if (response.status === 200) {
      // Redirect to login page
      window.location.href = '/login';
    } else {
      console.error('Unexpected logout response:', response);
    }
  } catch (error) {
    console.error('Logout failed:', error);
  }
};

export default handleLogout;
