// src/components/Header.jsx
import React from 'react';
import './Header.css';
// Assume you've saved the logo in the assets folder
import logo from '../assets/ODC_logo.jpeg'; 

const Header = () => {
  return (
    <header className="header-principal">
      <div className="logo">
        <img src={logo} alt="Logo Orange" />
        <span>Digital Center</span>
      </div>
      <button className="btn-connexion">Connexion</button>
    </header>
  );
};

export default Header;