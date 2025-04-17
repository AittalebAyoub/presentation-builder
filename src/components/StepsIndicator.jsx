// src/components/StepsIndicator.jsx
import React from 'react';

const StepsIndicator = ({ currentStep }) => {
  const steps = [
    { number: 1, title: 'Configuration' },
    { number: 2, title: 'Plan de formation' },
    { number: 3, title: 'Génération' }
  ];
  
  return (
    <div className="steps">
      {steps.map((step) => (
        <div 
          key={step.number}
          className={`step ${
            step.number === currentStep 
              ? 'active' 
              : step.number < currentStep 
                ? 'completed' 
                : ''
          }`}
        >
          <div className="step-number">{step.number}</div>
          <div className="step-title">{step.title}</div>
        </div>
      ))}
    </div>
  );
};

export default StepsIndicator;