// src/components/QuizGeneration.jsx
import React from 'react';

const QuizGeneration = ({ progress = 65 }) => {
  return (
    <div className="quiz-loading fade-in" style={{ textAlign: 'center' }}>
      <div style={{ marginBottom: '2rem' }}>
        {/* Simple CSS spinner */}
        <div className="spinner" style={{
          width: '48px',
          height: '48px',
          border: '5px solid #f3f3f3',
          borderTop: '5px solid var(--primary)',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite',
          margin: '0 auto'
        }}></div>
        <style jsx>{`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}</style>
      </div>
      <p style={{ fontSize: '1.2rem', marginBottom: '1rem' }}>
        Génération des quiz en cours...
      </p>
      <p style={{ color: 'var(--text-light)' }}>
        Cette opération peut prendre jusqu'à une minute.
      </p>
      
      <div style={{ width: '80%', margin: '2rem auto', marginBottom: '20px' }}>
        <div style={{ 
          height: '10px', 
          backgroundColor: '#E2E8F0', 
          borderRadius: '5px',
          overflow: 'hidden'
        }}>
          <div style={{ 
            height: '100%', 
            width: `${progress}%`, 
            background: 'linear-gradient(135deg, var(--primary) 0%, #FFA64D 100%)',
            borderRadius: '5px',
            transition: 'width 0.5s ease'
          }}></div>
        </div>
        <p style={{ marginTop: '10px', fontSize: '0.9rem', color: 'var(--text-light)' }}>
          {progress}% terminé
        </p>
      </div>
    </div>
  );
};

export default QuizGeneration;