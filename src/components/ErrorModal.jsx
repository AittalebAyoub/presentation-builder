// src/components/ErrorModal.jsx
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes, faExclamationTriangle } from '@fortawesome/free-solid-svg-icons';

const ErrorModal = ({ message, onClose }) => {
  return (
    <div className="modal">
      <div className="modal-content">
        <div className="modal-header">
          <h3>
            <FontAwesomeIcon icon={faExclamationTriangle} style={{ color: 'var(--danger)', marginRight: '10px' }} />
            Erreur
          </h3>
          <button 
            type="button" 
            className="close-modal" 
            onClick={onClose}
          >
            <FontAwesomeIcon icon={faTimes} />
          </button>
        </div>
        
        <div className="modal-body">
          <p style={{ color: 'var(--text)', fontSize: '1.1rem', lineHeight: '1.6' }}>
            {message || "Une erreur s'est produite. Veuillez réessayer."}
          </p>
        </div>
        
        <div className="modal-footer">
          <button 
            type="button" 
            className="btn btn-primary" 
            onClick={onClose}
          >
            OK
          </button>
        </div>
      </div>
    </div>
  );
};

export default ErrorModal;