// src/components/Step2Plan.jsx
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faArrowUp, 
  faArrowDown, 
  faEdit, 
  faFileCirclePlus, 
  faArrowLeft, 
  faWandMagicSparkles 
} from '@fortawesome/free-solid-svg-icons';

const Step2Plan = ({ 
  sections, 
  onMoveSection, 
  onEditSection, 
  onAddSection, 
  onPrevious, 
  onNext 
}) => {
  return (
    <div className="card">
      <h2>Plan de la présentation</h2>
      <div id="planContent" className="mt-4">
        {sections.map((section, index) => (
          <div 
            key={section.id} 
            className="plan-item" 
            data-section-id={section.id}
          >
            <h3>{index + 1}. {section.title}</h3>
            <div className="order-actions">
              <button 
                type="button" 
                className="btn btn-sm btn-secondary" 
                onClick={() => onMoveSection(section.id, 'up')} 
                title="Déplacer vers le haut"
              >
                <FontAwesomeIcon icon={faArrowUp} />
              </button>
              <button 
                type="button" 
                className="btn btn-sm btn-secondary" 
                onClick={() => onMoveSection(section.id, 'down')} 
                title="Déplacer vers le bas"
              >
                <FontAwesomeIcon icon={faArrowDown} />
              </button>
            </div>
            <div className="plan-actions">
              <button 
                type="button" 
                className="btn btn-sm btn-warning" 
                onClick={() => onEditSection(section.id)}
              >
                <FontAwesomeIcon icon={faEdit} />
              </button>
            </div>
            {section.subsections && Array.isArray(section.subsections) && section.subsections.length > 0 && (
              <ul>
                {section.subsections.map((subsection, idx) => (
                  <li key={idx}>{subsection}</li>
                ))}
              </ul>
            )}
          </div>
        ))}
      </div>
      
      <div className="add-button-container">
        <button 
          type="button" 
          className="btn btn-success" 
          onClick={onAddSection}
        >
          <FontAwesomeIcon icon={faFileCirclePlus} />
          <span>Ajouter une section</span>
        </button>
      </div>
      
      <div className="actions">
        <button 
          type="button" 
          className="btn btn-secondary" 
          onClick={onPrevious}
        >
          <FontAwesomeIcon icon={faArrowLeft} />
          <span>Retour</span>
        </button>
        <button 
          type="button" 
          className="btn btn-primary" 
          onClick={onNext}
        >
          <span>Valider et générer</span>
          <FontAwesomeIcon icon={faWandMagicSparkles} />
        </button>
      </div>
    </div>
  );
};

export default Step2Plan;