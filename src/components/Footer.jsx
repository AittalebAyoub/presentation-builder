// src/components/Footer.jsx
import React from 'react';
import './Footer.css';

const Footer = () => {
  return (
    <footer>
      <div className="footer-left">
        <span>© 2025 MonSite</span>
        <a href="#accessibility">Accessibilité</a>
        <a href="#contact">Contact</a>
      </div>
      <div className="footer-right">
        <a href="#external">Lien externe ↗</a>
      </div>
    </footer>
  );
};

export default Footer;