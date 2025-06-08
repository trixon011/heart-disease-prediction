const API_URL =
  process.env.NODE_ENV === 'production'
    ? 'https://backend-deployed-5jr1.onrender.com/api'
    : 'http://127.0.0.1:5000/api';

export default API_URL;