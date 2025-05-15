// src/components/QuizSuccess.jsx
import React from 'react';

const QuizSuccess = ({ quizResults, onClose }) => {
  // Helper to render quiz items from results
  const renderQuizItems = () => {
    if (!quizResults || !quizResults.forms || quizResults.forms.length === 0) {
      return (
        <div style={{ padding: '1rem', backgroundColor: '#FEF2F2', borderRadius: 'var(--radius-sm)', marginBottom: '1rem' }}>
          <p style={{ color: '#B91C1C' }}>Aucun quiz n'a été généré.</p>
        </div>
      );
    }

    return quizResults.forms.map((form, index) => {
      if (!form) return null;
      
      return (
        <div 
          key={index}
          className="quiz-item" 
          style={{ 
            padding: '1rem', 
            borderRadius: 'var(--radius-sm)', 
            backgroundColor: '#F8FAFC',
            marginBottom: '1rem',
            border: '1px solid var(--border)'
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h4>{form.title || `Quiz ${index + 1}`}</h4>
            <div style={{ display: 'flex', gap: '10px' }}>
              <a 
                href={form.view_url} 
                className="btn btn-sm btn-secondary"
                target="_blank"
                rel="noopener noreferrer"
              >
                <span>Voir</span>
              </a>
              {form.edit_url && (
                <a 
                  href={form.edit_url} 
                  className="btn btn-sm btn-warning"
                  target="_blank"
                  rel="noopener noreferrer"
                >
                  <span>Éditer</span>
                </a>
              )}
            </div>
          </div>
        </div>
      );
    });
  };

  // Render notifications status
  const renderNotificationsStatus = () => {
    if (!quizResults || !quizResults.shared_with) return null;
    
    const { successful = [], failed = [] } = quizResults.shared_with;
    
    if (successful.length === 0 && failed.length === 0) return null;
    
    return (
      <div style={{ 
        padding: '1rem', 
        backgroundColor: successful.length > 0 ? '#F0FDF4' : '#FEF2F2', 
        borderRadius: 'var(--radius-sm)',
        marginBottom: '2rem',
        border: `1px solid ${successful.length > 0 ? '#DCFCE7' : '#FEE2E2'}`
      }}>
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '10px', 
          marginBottom: '0.5rem' 
        }}>
          {/* Email icon using HTML/CSS */}
          <div style={{ 
            width: '20px', 
            height: '16px', 
            position: 'relative', 
            backgroundColor: successful.length > 0 ? 'var(--success)' : 'var(--danger)',
            maskImage: 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 512 512\'%3E%3Cpath d=\'M48 64C21.5 64 0 85.5 0 112c0 15.1 7.1 29.3 19.2 38.4L236.8 313.6c11.4 8.5 27 8.5 38.4 0L492.8 150.4c12.1-9.1 19.2-23.3 19.2-38.4c0-26.5-21.5-48-48-48H48zM0 176V384c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V176L294.4 339.2c-22.8 17.1-54 17.1-76.8 0L0 176z\'/%3E%3C/svg%3E")',
            WebkitMaskImage: 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 512 512\'%3E%3Cpath d=\'M48 64C21.5 64 0 85.5 0 112c0 15.1 7.1 29.3 19.2 38.4L236.8 313.6c11.4 8.5 27 8.5 38.4 0L492.8 150.4c12.1-9.1 19.2-23.3 19.2-38.4c0-26.5-21.5-48-48-48H48zM0 176V384c0 35.3 28.7 64 64 64H448c35.3 0 64-28.7 64-64V176L294.4 339.2c-22.8 17.1-54 17.1-76.8 0L0 176z\'/%3E%3C/svg%3E")',
            maskRepeat: 'no-repeat',
            WebkitMaskRepeat: 'no-repeat',
            maskSize: 'contain',
            WebkitMaskSize: 'contain'
          }} />
          <p style={{ margin: 0, fontWeight: '500' }}>
            {successful.length > 0 ? 'Emails envoyés avec succès' : 'Erreur d\'envoi d\'emails'}
          </p>
        </div>
        
        {successful.length > 0 && (
          <p style={{ margin: 0, color: 'var(--text-light)', fontSize: '0.9rem' }}>
            Les notifications ont été envoyées à {successful.length} destinataire(s).
          </p>
        )}
        
        {failed.length > 0 && (
          <p style={{ margin: 0, color: 'var(--danger)', fontSize: '0.9rem' }}>
            Échec d'envoi à {failed.length} destinataire(s).
          </p>
        )}
      </div>
    );
  };

  return (
    <div className="quiz-success fade-in card">
      <h2>Génération de Quiz</h2>
      <div style={{ padding: '2rem 1rem' }}>
        <div style={{ 
          marginBottom: '2rem', 
          color: 'var(--success)', 
          fontSize: '4rem', 
          textAlign: 'center' 
        }}>
          {/* Checkmark icon using HTML/CSS */}
          <div style={{ 
            width: '64px', 
            height: '64px', 
            margin: '0 auto',
            backgroundColor: 'var(--success)',
            maskImage: 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 512 512\'%3E%3Cpath d=\'M256 512c141.4 0 256-114.6 256-256S397.4 0 256 0S0 114.6 0 256S114.6 512 256 512zM369 209L241 337c-9.4 9.4-24.6 9.4-33.9 0l-64-64c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0l47 47L335 175c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9z\'/%3E%3C/svg%3E")',
            WebkitMaskImage: 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 512 512\'%3E%3Cpath d=\'M256 512c141.4 0 256-114.6 256-256S397.4 0 256 0S0 114.6 0 256S114.6 512 256 512zM369 209L241 337c-9.4 9.4-24.6 9.4-33.9 0l-64-64c-9.4-9.4-9.4-24.6 0-33.9s24.6-9.4 33.9 0l47 47L335 175c9.4-9.4 24.6-9.4 33.9 0s9.4 24.6 0 33.9z\'/%3E%3C/svg%3E")',
            maskRepeat: 'no-repeat',
            WebkitMaskRepeat: 'no-repeat',
            maskSize: 'contain',
            WebkitMaskSize: 'contain'
          }} />
        </div>
        
        <h3 style={{ marginBottom: '1.5rem', textAlign: 'center' }}>
          Les quiz ont été générés avec succès!
        </h3>
        
        <div className="quiz-list" style={{ marginBottom: '2rem' }}>
          {renderQuizItems()}
        </div>
        
        {renderNotificationsStatus()}
        
        <div className="actions" style={{ marginTop: '2rem' }}>
          <button 
            type="button" 
            className="btn btn-secondary" 
            onClick={onClose}
          >
            Retour
          </button>
        </div>
      </div>
    </div>
  );
};

export default QuizSuccess;