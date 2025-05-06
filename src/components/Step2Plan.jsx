// src/components/Step2Plan.jsx
import React, { useState } from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { 
  faArrowUp, 
  faArrowDown, 
  faEdit, 
  faFileCirclePlus, 
  faArrowLeft, 
  faWandMagicSparkles,
  faChevronDown,
  faChevronUp,
  faPlus,
  faCalendarPlus
} from '@fortawesome/free-solid-svg-icons';

const Step2Plan = ({ 
  sections, 
  planType,
  onMoveSection, 
  onEditSection, 
  onAddSection,
  onAddSession,
  onAddDay,
  onPrevious, 
  onNext 
}) => {
  const [expandedDays, setExpandedDays] = useState({});
  
  const toggleDayExpansion = (dayId) => {
    setExpandedDays({
      ...expandedDays,
      [dayId]: !expandedDays[dayId]
    });
  };
  
  // Check if we're using the day-based format
  const isDayFormat = planType === 'jour' || sections.some(section => section.isDay);
  
  return (
    <div className="card">
      <h2>Plan de la présentation</h2>
      <div id="planContent" className="mt-4">
        {isDayFormat ? (
          // Day-based plan format
          sections.map((day, dayIndex) => (
            <div 
              key={day.id} 
              className="plan-item day-item"
              style={{ marginBottom: '1.5rem' }}
            >
              <div 
                className="day-header" 
                style={{ 
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '0.5rem',
                  backgroundColor: '#f8f9fa',
                  borderRadius: '5px',
                  borderLeft: '4px solid var(--primary)',
                  cursor: 'pointer'
                }}
                onClick={() => toggleDayExpansion(day.id)}
              >
                <h3 style={{ margin: 0 }}>Jour {day.day}</h3>
                <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
                  <div className="order-actions">
                    <button 
                      type="button" 
                      className="btn btn-sm btn-secondary" 
                      onClick={(e) => {
                        e.stopPropagation();
                        onMoveSection(day.id, 'up');
                      }} 
                      title="Déplacer vers le haut"
                    >
                      <FontAwesomeIcon icon={faArrowUp} />
                    </button>
                    <button 
                      type="button" 
                      className="btn btn-sm btn-secondary" 
                      onClick={(e) => {
                        e.stopPropagation();
                        onMoveSection(day.id, 'down');
                      }} 
                      title="Déplacer vers le bas"
                    >
                      <FontAwesomeIcon icon={faArrowDown} />
                    </button>
                  </div>
                  <FontAwesomeIcon 
                    icon={expandedDays[day.id] ? faChevronUp : faChevronDown} 
                  />
                </div>
              </div>
              
              {expandedDays[day.id] && (
                <div className="day-content" style={{ marginTop: '1rem', paddingLeft: '1.5rem' }}>
                  {day.sessions && day.sessions.map((session, sessionIndex) => (
                    <div 
                      key={session.id} 
                      className="plan-item session-item" 
                      style={{ 
                        marginBottom: '1.5rem',
                        padding: '1rem',
                        backgroundColor: '#ffffff',
                        border: '1px solid #e9ecef',
                        borderRadius: '5px',
                        position: 'relative'
                      }}
                    >
                      <h3>{sessionIndex + 1}. {session.title}</h3>
                      <div className="order-actions" style={{ position: 'absolute', top: '1rem', right: '5rem' }}>
                        <button 
                          type="button" 
                          className="btn btn-sm btn-secondary" 
                          onClick={() => onMoveSection(session.id, 'up')} 
                          title="Déplacer vers le haut"
                        >
                          <FontAwesomeIcon icon={faArrowUp} />
                        </button>
                        <button 
                          type="button" 
                          className="btn btn-sm btn-secondary" 
                          onClick={() => onMoveSection(session.id, 'down')} 
                          title="Déplacer vers le bas"
                        >
                          <FontAwesomeIcon icon={faArrowDown} />
                          </button>
                      </div>
                      <div className="plan-actions" style={{ position: 'absolute', top: '1rem', right: '1rem' }}>
                        <button 
                          type="button" 
                          className="btn btn-sm btn-warning" 
                          onClick={() => onEditSection(session.id)}
                        >
                          <FontAwesomeIcon icon={faEdit} />
                        </button>
                      </div>
                      {session.subsections && Array.isArray(session.subsections) && session.subsections.length > 0 && (
                        <ul>
                          {session.subsections.map((subsection, idx) => (
                            <li key={idx}>{subsection}</li>
                          ))}
                        </ul>
                      )}
                    </div>
                  ))}
                  
                  <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
                    <button 
                      type="button" 
                      className="btn btn-sm btn-secondary" 
                      onClick={() => onAddSession(day.id)}
                    >
                      <FontAwesomeIcon icon={faPlus} />
                      <span style={{ marginLeft: '5px' }}>Ajouter une session</span>
                    </button>
                  </div>
                </div>
              )}
            </div>
          ))
        ) : (
          // Original section-based plan format
          sections.map((section, index) => (
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
          ))
        )}
      </div>
      
      <div className="add-button-container">
        {isDayFormat ? (
          <button 
            type="button" 
            className="btn btn-success" 
            onClick={onAddDay}
          >
            <FontAwesomeIcon icon={faCalendarPlus} />
            <span>Ajouter un jour</span>
          </button>
        ) : (
          <button 
            type="button" 
            className="btn btn-success" 
            onClick={onAddSection}
          >
            <FontAwesomeIcon icon={faFileCirclePlus} />
            <span>Ajouter une section</span>
          </button>
        )}
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