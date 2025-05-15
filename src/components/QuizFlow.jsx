// src/components/QuizFlow.jsx
import React, { useState } from 'react';
import QuizConfiguration from './QuizConfiguration';
import QuizGeneration from './QuizGeneration';
import QuizSuccess from './QuizSuccess';

/**
 * Main component that manages the quiz generation flow
 */
const QuizFlow = ({ 
  content, 
  planType, 
  subject, 
  onCancel, 
  onError 
}) => {
  // State management for quiz generation flow
  const [step, setStep] = useState('config'); // config, generating, success
  const [quizProgress, setQuizProgress] = useState(0);
  const [quizResults, setQuizResults] = useState(null);
  const [currentDay, setCurrentDay] = useState(null);
  
  // Process the section content for quiz generation
  const processContent = (content) => {
    if (!content) return [];
    
    // If it's already in the right format, return as is
    if (Array.isArray(content)) return content;
    
    // Try to convert from API response format
    if (content.content && Array.isArray(content.content)) {
      return content.content;
    }
    
    return [];
  };
  
  // Handle quiz configuration submission
  const handleSubmit = async (quizConfig) => {
    try {
      setStep('generating');
      setQuizProgress(10);
      
      const processedContent = processContent(content);
      
      // Simulate progress
      const progressInterval = setInterval(() => {
        setQuizProgress(prev => {
          const nextProgress = prev + 5;
          return nextProgress > 90 ? 90 : nextProgress;
        });
      }, 1000);
      
      // Simulate API calls for demo purposes
      // In a real application, replace this with actual API calls
      setTimeout(() => {
        clearInterval(progressInterval);
        setQuizProgress(100);
        
        // Sample quiz results that would come from an API
        const mockQuizResults = {
          success: true,
          forms: [
            {
              form_id: 'form1',
              title: `Quiz: ${subject} - Section 1`,
              view_url: 'https://docs.google.com/forms/d/e/sample1/viewform',
              edit_url: 'https://docs.google.com/forms/d/e/sample1/edit'
            },
            {
              form_id: 'form2',
              title: `Quiz: ${subject} - Section 2`,
              view_url: 'https://docs.google.com/forms/d/e/sample2/viewform',
              edit_url: 'https://docs.google.com/forms/d/e/sample2/edit'
            }
          ],
          shared_with: {
            successful: quizConfig.emails.concat(quizConfig.trainerEmails),
            failed: []
          }
        };
        
        // Small delay to show the 100% progress
        setTimeout(() => {
          setQuizResults(mockQuizResults);
          setStep('success');
        }, 500);
      }, 3000);
      
    } catch (error) {
      console.error('Error in quiz generation flow:', error);
      if (onError) {
        onError(error.message || 'An error occurred during quiz generation');
      }
      setStep('config');
    }
  };
  
  // Render different components based on the current step
  switch (step) {
    case 'generating':
      return (
        <div className="card">
          <h2>Génération de Quiz</h2>
          <div style={{ padding: '2rem 1rem' }}>
            <QuizGeneration progress={quizProgress} currentDay={currentDay} />
          </div>
        </div>
      );
    
    case 'success':
      return <QuizSuccess quizResults={quizResults} onClose={onCancel} />;
    
    case 'config':
    default:
      return (
        <div className="card">
          <h2>Configuration du Quiz</h2>
          <div style={{ padding: '2rem 1rem' }}>
            <QuizConfiguration 
              onCancel={onCancel} 
              onSubmit={handleSubmit} 
              planType={planType} 
            />
          </div>
        </div>
      );
  }
};

export default QuizFlow;