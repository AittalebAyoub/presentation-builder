// src/components/Step3Generation.jsx
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faCheckCircle, faDownload } from '@fortawesome/free-solid-svg-icons';

const Step3Generation = ({ isGenerating }) => {
  return (
    <div className="card">
      <h2>Génération de la présentation</h2>
      <div style={{ textAlign: 'center', padding: '4rem 0' }}>
        {isGenerating ? (
          <div id="loading" className="loading-animation">
            <div style={{ marginBottom: '2rem' }}>
              <svg width="80" height="80" viewBox="0 0 80 80">
                <circle 
                  cx="40" 
                  cy="40" 
                  r="30" 
                  fill="none" 
                  stroke="url(#gradient)" 
                  strokeWidth="6" 
                  strokeLinecap="round" 
                  strokeDasharray="188.5" 
                  strokeDashoffset="0"
                >
                  <animateTransform 
                    attributeName="transform" 
                    type="rotate" 
                    dur="1.5s" 
                    from="0 40 40" 
                    to="360 40 40" 
                    repeatCount="indefinite" 
                  />
                </circle>
                <defs>
                  <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                    <stop offset="0%" stopColor="#FF7900" />
                    <stop offset="100%" stopColor="#FFA64D" />
                  </linearGradient>
                </defs>
              </svg>
            </div>
            <p style={{ fontSize: '1.2rem', color: 'var(--text-light)' }}>
              Génération de votre présentation en cours...
            </p>
          </div>
        ) : (
          <div id="completed" className="fade-in">
            <div style={{ marginBottom: '2rem', color: 'var(--success)', fontSize: '5rem' }}>
              <FontAwesomeIcon icon={faCheckCircle} />
            </div>
            <p style={{ fontSize: '1.5rem', fontWeight: '600', marginBottom: '1rem', color: 'var(--text)' }}>
              Votre présentation a été générée avec succès!
            </p>
            <p style={{ color: 'var(--text-light)', marginBottom: '2rem' }}>
              Le fichier est prêt à être téléchargé
            </p>
            <button type="button" className="btn btn-success" style={{ marginTop: '1rem', padding: '0.9rem 2rem' }}>
              <FontAwesomeIcon icon={faDownload} />
              <span>Télécharger la présentation</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Step3Generation;