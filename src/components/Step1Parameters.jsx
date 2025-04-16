// src/components/Step1Parameters.jsx
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowRight, faSpinner } from '@fortawesome/free-solid-svg-icons';

const Step1Parameters = ({ formData, onChange, onNext, isLoading }) => {
  return (
    <div className="card slide-up">
      <form id="parametersForm">
        <div className="form-group">
          <label htmlFor="subject">Sujet de la présentation</label>
          <input 
            type="text" 
            id="subject" 
            name="subject"
            className="form-control" 
            placeholder="Ex: Introduction à Python" 
            value={formData.subject} 
            onChange={onChange}
            required 
            disabled={isLoading}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="level">Niveau des apprenants</label>
          <select 
            id="level" 
            name="level"
            className="form-control" 
            value={formData.level} 
            onChange={onChange}
            required
            disabled={isLoading}
          >
            <option value="" disabled>Sélectionnez un niveau</option>
            <option value="debutant">Débutant</option>
            <option value="intermediaire">Intermédiaire</option>
            <option value="avance">Avancé</option>
            <option value="expert">Expert</option>
          </select>
        </div>
        
        <div className="form-group">
          <label htmlFor="planType">Type de plan</label>
          <select 
            id="planType" 
            name="planType"
            className="form-control" 
            value={formData.planType} 
            onChange={onChange}
            required
            disabled={isLoading}
          >
            <option value="" disabled>Sélectionnez un type de plan</option>
            <option value="section">Section</option>
            <option value="brut">Brut</option>
            <option value="jour">Par jour</option>
          </select>
        </div>
        
        <div className="form-group">
          <label htmlFor="trainerName">Nom du formateur</label>
          <input 
            type="text" 
            id="trainerName" 
            name="trainerName"
            className="form-control" 
            placeholder="Votre nom (utilisé sur la présentation)" 
            value={formData.trainerName} 
            onChange={onChange}
            disabled={isLoading}
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="description">Description / Prompt</label>
          <textarea 
            id="description" 
            name="description"
            className="form-control" 
            placeholder="Décrivez le contenu souhaité pour votre présentation..." 
            value={formData.description} 
            onChange={onChange}
            disabled={isLoading}
          />
        </div>
        
        <div className="form-group">
          <label>Format de fichier</label>
          <div className="radio-group">
            <div className="radio-option">
              <input 
                type="radio" 
                id="format-pdf" 
                name="format" 
                value="pdf" 
                checked={formData.format === 'pdf'} 
                onChange={onChange}
                disabled={isLoading}
              />
              <label htmlFor="format-pdf">PDF</label>
            </div>
            <div className="radio-option">
              <input 
                type="radio" 
                id="format-pptx" 
                name="format" 
                value="pptx" 
                checked={formData.format === 'pptx'} 
                onChange={onChange}
                disabled={isLoading}
              />
              <label htmlFor="format-pptx">PPTX</label>
            </div>
            <div className="radio-option">
              <input 
                type="radio" 
                id="format-both" 
                name="format" 
                value="both" 
                checked={formData.format === 'both'} 
                onChange={onChange}
                disabled={isLoading}
              />
              <label htmlFor="format-both">PDF & PPTX</label>
            </div>
          </div>
        </div>
        
        <div className="actions">
          <div></div> {/* Empty div for spacing */}
          <button 
            type="button" 
            className={`btn btn-primary ${isLoading ? 'loading' : ''}`} 
            onClick={onNext}
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <span>Génération en cours...</span>
                <FontAwesomeIcon icon={faSpinner} spin />
              </>
            ) : (
              <>
                <span>Suivant</span>
                <FontAwesomeIcon icon={faArrowRight} />
              </>
            )}
          </button>
        </div>
      </form>
    </div>
  );
};

export default Step1Parameters;