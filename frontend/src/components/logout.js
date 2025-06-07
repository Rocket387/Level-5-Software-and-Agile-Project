import axios from 'axios';
import { logout } from '../api';  

const handleLogout = async (navigate) => {  
  try {
    const confirmLogout = window.confirm('Are you sure you want to log out?');
    if (!confirmLogout) {
      console.log('Logout cancelled by user.');
      return;
    }
    const response = await logout();
    if (response.status === 200) {
      console.log('Logout successful, navigating to login...');
      navigate('/login'); 
    } else {
      console.error('Unexpected logout response:', response);
    }
  } catch (error) {
    console.error('Logout failed:', error);
  }
};

export default handleLogout;
