// src/components/Step3Generation.jsx
import React from 'react';
import QuizButton from './QuizButton';

const Step3Generation = ({ 
  isGenerating, 
  progress = 0, 
  filesResponse, 
  onDownload, 
  currentDay,
  onGenerateQuiz // New prop for quiz generation
}) => {
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
              {/* Checkmark icon using CSS */}
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
                  {/* PDF icon using CSS */}
                  <div style={{ 
                    display: 'inline-block',
                    width: '16px', 
                    height: '16px', 
                    marginRight: '10px',
                    backgroundColor: 'white',
                    maskImage: 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 384 512\'%3E%3Cpath d=\'M320 464c8.8 0 16-7.2 16-16V160H256c-17.7 0-32-14.3-32-32V48H64c-8.8 0-16 7.2-16 16V448c0 8.8 7.2 16 16 16H320zM0 64C0 28.7 28.7 0 64 0H229.5c17 0 33.3 6.7 45.3 18.7l90.5 90.5c12 12 18.7 28.3 18.7 45.3V448c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V64z\'/%3E%3C/svg%3E")',
                    WebkitMaskImage: 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 384 512\'%3E%3Cpath d=\'M320 464c8.8 0 16-7.2 16-16V160H256c-17.7 0-32-14.3-32-32V48H64c-8.8 0-16 7.2-16 16V448c0 8.8 7.2 16 16 16H320zM0 64C0 28.7 28.7 0 64 0H229.5c17 0 33.3 6.7 45.3 18.7l90.5 90.5c12 12 18.7 28.3 18.7 45.3V448c0 35.3-28.7 64-64 64H64c-35.3 0-64-28.7-64-64V64z\'/%3E%3C/svg%3E")',
                    maskRepeat: 'no-repeat',
                    WebkitMaskRepeat: 'no-repeat',
                    maskSize: 'contain',
                    WebkitMaskSize: 'contain'
                  }} />
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
                  {/* PowerPoint icon using CSS */}
                  <div style={{ 
                    display: 'inline-block',
                    width: '16px', 
                    height: '16px', 
                    marginRight: '10px',
                    backgroundColor: '#9A3412',
                    maskImage: 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 384 512\'%3E%3Cpath d=\'M64 0C28.7 0 0 28.7 0 64V448c0 35.3 28.7 64 64 64H320c35.3 0 64-28.7 64-64V160H256c-17.7 0-32-14.3-32-32V0H64zM256 0V128H384L256 0zM136 240h68c42 0 76 34 76 76s-34 76-76 76H160v32c0 13.3-10.7 24-24 24s-24-10.7-24-24V264c0-13.3 10.7-24 24-24zm68 104c15.5 0 28-12.5 28-28s-12.5-28-28-28H160v56h44z\'/%3E%3C/svg%3E")',
                    WebkitMaskImage: 'url("data:image/svg+xml,%3Csvg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 384 512\'%3E%3Cpath d=\'M64 0C28.7 0 0 28.7 0 64V448c0 35.3 28.7 64 64 64H320c35.3 0 64-28.7 64-64V160H256c-17.7 0-32-14.3-32-32V0H64zM256 0V128H384L256 0zM136 240h68c42 0 76 34 76 76s-34 76-76 76H160v32c0 13.3-10.7 24-24 24s-24-10.7-24-24V264c0-13.3 10.7-24 24-24zm68 104c15.5 0 28-12.5 28-28s-12.5-28-28-28H160v56h44z\'/%3E%3C/svg%3E")',
                    maskRepeat: 'no-repeat',
                    WebkitMaskRepeat: 'no-repeat',
                    maskSize: 'contain',
                    WebkitMaskSize: 'contain'
                  }} />
                  <span>Télécharger PowerPoint</span>
                </button>
              )}
              
              {(!pdfFile && !pptxFile) && (
                <button type="button" className="btn btn-secondary" disabled>
                  <span>Aucun fichier disponible</span>
                </button>
              )}
            </div>
            
            {/* Add Quiz Button - This is the new part */}
            <QuizButton onClick={onGenerateQuiz} />
          </div>
        )}
      </div>
    </div>
  );
};

export default Step3Generation;