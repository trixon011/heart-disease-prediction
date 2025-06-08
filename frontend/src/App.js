import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';
import Home from './components/Home';
import Predict from './components/Predict';
import Footer from './components/Footer';
import Login from './components/Login';
import Signup from './components/Signup';
import './App.css';

function App() {
  return (
    <Router>
      <Navbar />
      <div className="test">
        <h1>Testing Login Render</h1>
        <Login />
      </div>
      <Footer />
    </Router>
  );
}


export default App;
