// src/components/LoadingSpinner.jsx
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSpinner } from '@fortawesome/free-solid-svg-icons';

const LoadingSpinner = ({ message }) => {
  return (
    <div className="loading-overlay">
      <div className="loading-spinner-container">
        <FontAwesomeIcon icon={faSpinner} spin size="3x" />
        <p>{message || 'Chargement en cours...'}</p>
      </div>
    </div>
  );
};

export default LoadingSpinner;