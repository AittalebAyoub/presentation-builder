// src/components/AddSessionModal.jsx
import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTimes, faTrashAlt, faCirclePlus, faSave } from '@fortawesome/free-solid-svg-icons';

const AddSessionModal = ({ dayId, onClose, onAdd }) => {
  const [title, setTitle] = useState('');
  const [subsections, setSubsections] = useState(['']);
  
  // Add a new subsection
  const addSubsection = () => {
    setSubsections([...subsections, '']);
  };
  
  // Remove a subsection
  const removeSubsection = (index) => {
    const newSubsections = [...subsections];
    newSubsections.splice(index, 1);
    setSubsections(newSubsections);
  };
  
  // Update a subsection
  const updateSubsection = (index, value) => {
    const newSubsections = [...subsections];
    newSubsections[index] = value;
    setSubsections(newSubsections);
  };
  
  // Handle add
  const handleAdd = () => {
    if (!title.trim()) {
      alert('Veuillez entrer un titre pour la session.');
      return;
    }
    
    // Filter out empty subsections
    const filteredSubsections = subsections.filter(sub => sub.trim() !== '');
    onAdd(dayId, title, filteredSubsections);
  };
  
  return (
    <div className="modal">
      <div className="modal-content">
        <div className="modal-header">
          <h3>Ajouter une nouvelle session</h3>
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
            <label htmlFor="newSessionTitle">Titre de la session</label>
            <input 
              type="text" 
              id="newSessionTitle" 
              className="form-control" 
              placeholder="Entrez le titre de la session"
              value={title} 
              onChange={(e) => setTitle(e.target.value)} 
            />
          </div>
          
          <div className="form-group">
            <label>Sous-sections</label>
            <div className="subsection-list">
              {subsections.map((subsection, index) => (
                <div key={index} className="subsection-item">
                  <input 
                    type="text" 
                    className="form-control" 
                    placeholder="Entrez une sous-section" 
                    value={subsection} 
                    onChange={(e) => updateSubsection(index, e.target.value)} 
                  />
                  <button 
                    type="button" 
                    className="btn btn-sm btn-danger" 
                    onClick={() => removeSubsection(index)}
                  >
                    <FontAwesomeIcon icon={faTrashAlt} />
                  </button>
                </div>
              ))}
            </div>
            
            <button 
              type="button" 
              className="btn btn-sm btn-secondary" 
              style={{ marginTop: '0.75rem' }} 
              onClick={addSubsection}
            >
              <FontAwesomeIcon icon={faCirclePlus} />
              <span>Ajouter une sous-section</span>
            </button>
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

export default AddSessionModal;