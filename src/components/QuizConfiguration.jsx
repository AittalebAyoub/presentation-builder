// src/components/QuizConfiguration.jsx
import React, { useState } from 'react';

const QuizConfiguration = ({ onCancel, onSubmit, planType }) => {
  const [quizConfig, setQuizConfig] = useState({
    type: planType === 'jour' ? 'day' : 'section',
    level: 'intermediaire',
    questionsPerItem: 5,
    recipientEmails: '',
    trainerEmails: '',
    sendEmails: true
  });
  
  // Handle form input changes
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setQuizConfig({
      ...quizConfig,
      [name]: type === 'checkbox' ? checked : value
    });
  };
  
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Process emails into arrays
    const emails = quizConfig.recipientEmails
      .split(',')
      .map(email => email.trim())
      .filter(email => email.length > 0);
    
    const trainerEmails = quizConfig.trainerEmails
      .split(',')
      .map(email => email.trim())
      .filter(email => email.length > 0);
    
    // Prepare data for submission
    const submitData = {
      ...quizConfig,
      emails,
      trainerEmails
    };
    
    onSubmit(submitData);
  };
  
  return (
    <div className="quiz-config fade-in">
      <h3 style={{ marginBottom: '1.5rem', color: 'var(--primary)' }}>Configuration du Quiz</h3>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="type">Type de quiz</label>
          <select 
            id="type" 
            name="type"
            className="form-control" 
            value={quizConfig.type} 
            onChange={handleInputChange}
          >
            <option value="section">Par section (un quiz pour chaque section)</option>
            <option value="day">Par jour (un quiz pour chaque jour)</option>
          </select>
        </div>
        
        <div className="form-group">
          <label htmlFor="level">Niveau de difficulté</label>
          <select 
            id="level" 
            name="level"
            className="form-control" 
            value={quizConfig.level} 
            onChange={handleInputChange}
          >
            <option value="debutant">Débutant</option>
            <option value="intermediaire">Intermédiaire</option>
            <option value="avance">Avancé</option>
          </select>
        </div>
        
        <div className="form-group">
          <label htmlFor="questionsPerItem">Nombre de questions par {quizConfig.type === 'section' ? 'section' : 'jour'}</label>
          <input 
            type="number" 
            id="questionsPerItem" 
            name="questionsPerItem"
            className="form-control" 
            value={quizConfig.questionsPerItem} 
            onChange={handleInputChange}
            min="1" 
            max="20"
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="sendEmails" style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
            <input 
              type="checkbox" 
              id="sendEmails" 
              name="sendEmails"
              checked={quizConfig.sendEmails} 
              onChange={handleInputChange}
              style={{ width: 'auto', margin: 0 }}
            />
            <span>Envoyer des notifications par email</span>
          </label>
        </div>
        
        {quizConfig.sendEmails && (
          <>
            <div className="form-group">
              <label htmlFor="recipientEmails">Emails des apprenants (séparés par des virgules)</label>
              <textarea 
                id="recipientEmails" 
                name="recipientEmails"
                className="form-control" 
                value={quizConfig.recipientEmails} 
                onChange={handleInputChange}
                placeholder="exemple@domaine.com, autre@domaine.com"
                rows="3"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="trainerEmails">Emails des formateurs (séparés par des virgules)</label>
              <textarea 
                id="trainerEmails" 
                name="trainerEmails"
                className="form-control" 
                value={quizConfig.trainerEmails} 
                onChange={handleInputChange}
                placeholder="formateur@domaine.com"
                rows="2"
              />
              <small style={{ color: 'var(--text-light)', display: 'block', marginTop: '5px' }}>
                Les formateurs auront les droits d'édition sur les formulaires.
              </small>
            </div>
          </>
        )}
        
        <div className="actions" style={{ marginTop: '2rem' }}>
          <button 
            type="button" 
            className="btn btn-secondary" 
            onClick={onCancel}
          >
            Annuler
          </button>
          <button 
            type="submit" 
            className="btn btn-primary" 
          >
            Générer le Quiz
          </button>
        </div>
      </form>
    </div>
  );
};

export default QuizConfiguration;