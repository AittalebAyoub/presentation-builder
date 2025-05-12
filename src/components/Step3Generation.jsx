// src/components/Step3Generation.jsx
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faCheckCircle, 
  faDownload, 
  faFilePdf, 
  faFilePowerpoint 
} from '@fortawesome/free-solid-svg-icons';

const Step3Generation = ({ isGenerating, progress = 0, filesResponse, onDownload, currentDay }) => {
  const getProgressText = (progressValue, currentDay) => {
    if (progressValue < 30) return 'Génération du plan...';
    if (progressValue < 70) {
      if (currentDay) {
        return `Création du contenu (Jour ${currentDay})...`;
      }
      return 'Création du contenu...';
    }
    return 'Création des fichiers...';
  };
  
  // Find PDF and PPTX files from response
  const pdfFile = filesResponse?.files?.find(file => file.type === 'pdf');
  const pptxFile = filesResponse?.files?.find(file => file.type === 'pptx');
  
  return (
    <div className="card">
      <h2>Génération de la présentation</h2>
      <div style={{ textAlign: 'center', padding: '4rem 0' }}>
        {isGenerating ? (
          <div id="loading" className="loading-animation">
            <div style={{ marginBottom: '2rem' }}>
              <svg width="80"
              height="80" 
              viewBox="0 0 80 80"
            >
              <circle 
                cx="40" 
                cy="40" 
                r="30" 
                fill="none" 
                stroke="url(#gradient)" 
                strokeWidth="6" 
                strokeLinecap="round" 
                strokeDasharray="188.5" 
                strokeDashoffset="0"
              >
                <animateTransform 
                  attributeName="transform" 
                  type="rotate" 
                  dur="1.5s" 
                  from="0 40 40" 
                  to="360 40 40" 
                  repeatCount="indefinite" 
                />
              </circle>
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="0%">
                  <stop offset="0%" stopColor="#FF7900" />
                  <stop offset="100%" stopColor="#FFA64D" />
                </linearGradient>
              </defs>
            </svg>
          </div>
          <div style={{ width: '80%', margin: '0 auto', marginBottom: '20px' }}>
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
          <p style={{ fontSize: '1.2rem', color: 'var(--text-light)' }}>
            {getProgressText(progress, currentDay)}
          </p>
        </div>
      ) : (
        <div id="completed" className="fade-in">
          <div style={{ marginBottom: '2rem', color: 'var(--success)', fontSize: '5rem' }}>
            <FontAwesomeIcon icon={faCheckCircle} />
          </div>
          <p style={{ fontSize: '1.5rem', fontWeight: '600', marginBottom: '1rem', color: 'var(--text)' }}>
            Votre présentation a été générée avec succès!
          </p>
          <p style={{ color: 'var(--text-light)', marginBottom: '2rem' }}>
            Les fichiers sont prêts à être téléchargés
          </p>
          
          <div style={{ display: 'flex', justifyContent: 'center', gap: '20px' }}>
            {pdfFile && (
              <button 
                type="button" 
                className="btn btn-success" 
                style={{ padding: '0.9rem 2rem' }}
                onClick={() => onDownload(pdfFile)}
              >
                <FontAwesomeIcon icon={faFilePdf} />
                <span>Télécharger PDF</span>
              </button>
            )}
            
            {pptxFile && (
              <button 
                type="button" 
                className="btn btn-warning" 
                style={{ padding: '0.9rem 2rem' }}
                onClick={() => onDownload(pptxFile)}
              >
                <FontAwesomeIcon icon={faFilePowerpoint} />
                <span>Télécharger PowerPoint</span>
              </button>
            )}
            
            {(!pdfFile && !pptxFile) && (
              <button type="button" className="btn btn-secondary" disabled>
                <FontAwesomeIcon icon={faDownload} />
                <span>Aucun fichier disponible</span>
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  </div>
  );
};

export default Step3Generation;