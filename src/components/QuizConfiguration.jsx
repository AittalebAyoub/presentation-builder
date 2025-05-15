// src/components/QuizConfiguration.jsx
import React, { useState } from 'react';

const QuizConfiguration = ({ onCancel, onSubmit, planType }) => {
  const [quizConfig, setQuizConfig] = useState({
    quizType: 'multiple', // 'multiple' or 'single'
    type: planType === 'jour' ? 'day' : 'section',
    level: 'intermediaire',
    questionsPerItem: 5,
    totalQuestions: 10, // For single quiz
    customContent: '', // For single quiz with custom content
    title: '', // For single quiz
    useCustomContent: false, // Whether to use custom content for single quiz
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
        {/* Quiz Type Selection */}
        <div className="form-group">
          <label htmlFor="quizType">Type de génération</label>
          <select 
            id="quizType" 
            name="quizType"
            className="form-control" 
            value={quizConfig.quizType} 
            onChange={handleInputChange}
          >
            <option value="multiple">Quiz multiples (un par section/jour)</option>
            <option value="single">Quiz unique (global)</option>
          </select>
        </div>
        
        {/* Configuration for Multiple Quizzes */}
        {quizConfig.quizType === 'multiple' && (
          <div className="form-group">
            <label htmlFor="type">Organisation des quiz</label>
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
        )}
        
        {/* Custom Content Option (for Single Quiz) */}
        {quizConfig.quizType === 'single' && (
          <div className="form-group">
            <label htmlFor="useCustomContent" style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
              <input 
                type="checkbox" 
                id="useCustomContent" 
                name="useCustomContent"
                checked={quizConfig.useCustomContent} 
                onChange={handleInputChange}
                style={{ width: 'auto', margin: 0 }}
              />
              <span>Utiliser un contenu personnalisé (au lieu du contenu de la présentation)</span>
            </label>
          </div>
        )}
        
        {/* Custom Content Text Area */}
        {quizConfig.quizType === 'single' && quizConfig.useCustomContent && (
          <div className="form-group">
            <label htmlFor="customContent">Contenu personnalisé</label>
            <textarea 
              id="customContent" 
              name="customContent"
              className="form-control" 
              value={quizConfig.customContent} 
              onChange={handleInputChange}
              placeholder="Entrez le contenu à partir duquel générer le quiz..."
              rows="6"
            />
          </div>
        )}
        
        {/* Title (for Single Quiz) */}
        {quizConfig.quizType === 'single' && (
          <div className="form-group">
            <label htmlFor="title">Titre du quiz</label>
            <input 
              type="text" 
              id="title" 
              name="title"
              className="form-control" 
              value={quizConfig.title} 
              onChange={handleInputChange}
              placeholder="Ex: Quiz sur Python"
            />
          </div>
        )}
        
        {/* Common Configuration Options */}
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
        
        {/* Questions Count */}
        {quizConfig.quizType === 'multiple' ? (
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
        ) : (
          <div className="form-group">
            <label htmlFor="totalQuestions">Nombre total de questions</label>
            <input 
              type="number" 
              id="totalQuestions" 
              name="totalQuestions"
              className="form-control" 
              value={quizConfig.totalQuestions} 
              onChange={handleInputChange}
              min="1" 
              max="30"
            />
          </div>
        )}
        
        {/* Email Notifications */}
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