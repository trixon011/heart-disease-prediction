const API_URL =
  process.env.NODE_ENV === 'production'
    ? 'https://heart-disease-prediction-3-u458.onrender.com/api'
    : 'http://127.0.0.1:5000/api';

export default API_URL;