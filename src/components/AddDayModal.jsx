// src/components/AddDayModal.jsx
import React, { useState, useEffect } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes, faSave } from '@fortawesome/free-solid-svg-icons';

const AddDayModal = ({ currentDays = [], onClose, onAdd }) => {
  const [dayNumber, setDayNumber] = useState(1);
  
  // When the modal opens, calculate the next available day number
  useEffect(() => {
    if (currentDays && currentDays.length > 0) {
      const maxDay = Math.max(...currentDays);
      setDayNumber(maxDay + 1);
    } else {
      setDayNumber(1);
    }
  }, [currentDays]);
  
  // Handle add
  const handleAdd = () => {
    if (dayNumber < 1) {
      alert('Veuillez entrer un numéro de jour valide (minimum 1).');
      return;
    }
    
    // Check if this day number already exists
    if (currentDays.includes(dayNumber)) {
      alert(`Le jour ${dayNumber} existe déjà. Veuillez choisir un autre numéro.`);
      return;
    }
    
    onAdd(dayNumber);
  };
  
  return (
    <div className="modal">
      <div className="modal-content">
        <div className="modal-header">
          <h3>Ajouter un nouveau jour</h3>
          <button 
            type="button" 
            className="close-modal" 
            onClick={onClose}
          >
            <FontAwesomeIcon icon={faTimes} />
          </button>
        </div>
        
        <div className="modal-body">
          <div className="form-group">
            <label htmlFor="dayNumber">Numéro du jour</label>
            <input 
              type="number" 
              id="dayNumber" 
              className="form-control" 
              placeholder="Ex: 3" 
              value={dayNumber} 
              onChange={(e) => setDayNumber(parseInt(e.target.value, 10))} 
              min="1"
              max="30"
            />
          </div>
        </div>
        
        <div className="modal-footer">
          <button 
            type="button" 
            className="btn btn-secondary" 
            onClick={onClose}
          >
            Annuler
          </button>
          <button 
            type="button" 
            className="btn btn-primary" 
            onClick={handleAdd}
          >
            <FontAwesomeIcon icon={faSave} />
            <span>Ajouter</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default AddDayModal;