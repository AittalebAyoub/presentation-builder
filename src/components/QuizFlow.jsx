// src/components/QuizFlow.jsx
import React, { useState } from 'react';
import QuizConfiguration from './QuizConfiguration';
import QuizGeneration from './QuizGeneration';
import QuizSuccess from './QuizSuccess';
import { 
  generateQuizzes, 
  generateSectionQuizzes, 
  generateDayQuizzes, 
  createMultipleForms, 
  shareQuizForms, 
  generateSingleQuiz 
} from '../services/api';

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
      
      // Determine if it's a single quiz or multiple quizzes
      const isSingleQuiz = quizConfig.quizType === 'single';
      
      // Start progress interval (simulate progress)
      const progressInterval = setInterval(() => {
        setQuizProgress(prev => {
          const nextProgress = prev + 5;
          return nextProgress > 90 ? 90 : nextProgress;
        });
      }, 1000);
      
      let quizResponse;
      
      if (isSingleQuiz) {
        // Generate a single comprehensive quiz
        setQuizProgress(20);
        
        // Use either custom content or the presentation content
        const quizContent = quizConfig.useCustomContent 
          ? quizConfig.customContent 
          : JSON.stringify(content);
        
        // Default the title if not provided
        const quizTitle = quizConfig.title || `Quiz sur ${subject}`;
        
        quizResponse = await generateSingleQuiz({
          content: quizContent,
          title: quizTitle,
          level: quizConfig.level,
          totalQuestions: parseInt(quizConfig.totalQuestions, 10),
          emails: quizConfig.emails,
          trainerEmails: quizConfig.trainerEmails
        });
        
        if (!quizResponse.success) {
          throw new Error(quizResponse.message || 'Failed to generate quiz');
        }
        
        // Format response to match multiple quiz format for consistent handling
        quizResponse = {
          success: true,
          forms: [quizResponse.form],
          quizzes: [quizResponse.quiz_data],
          shared_with: quizResponse.shared_with
        };
      } else {
        // Complete workflow for multiple quizzes (generate quizzes, create forms, share)
        const processedContent = processContent(content);
        
        if (quizConfig.type === 'section') {
          // For section-based quizzes, we use a multi-step process
          
          // Step 1: Generate quizzes for each section
          setQuizProgress(20);
          const quizzesResponse = await generateSectionQuizzes({
            content: processedContent,
            level: quizConfig.level,
            questionsPerItem: parseInt(quizConfig.questionsPerItem, 10),
            titleTemplate: subject
          });
          
          if (!quizzesResponse.success) {
            throw new Error(quizzesResponse.message || 'Failed to generate section quizzes');
          }
          
          // Step 2: Create Google Forms for each quiz
          setQuizProgress(50);
          const formsResponse = await createMultipleForms({
            quizDataList: quizzesResponse.quizzes,
            titleTemplate: subject,
            type: 'section'
          });
          
          if (!formsResponse.success) {
            throw new Error(formsResponse.message || 'Failed to create quiz forms');
          }
          
          // Step 3: Share forms with users if requested
          setQuizProgress(80);
          let shareResponse = { success: true };
          
          if (quizConfig.sendEmails && (quizConfig.emails.length > 0 || quizConfig.trainerEmails.length > 0)) {
            // For each form, share with the users
            const sharePromises = formsResponse.forms.filter(form => form).map(form => 
              shareQuizForms({
                formId: form.form_id,
                emails: quizConfig.emails,
                trainerEmails: quizConfig.trainerEmails,
                title: form.title,
                editUrl: form.edit_url,
                viewUrl: form.view_url
              })
            );
            
            // Wait for all sharing operations to complete
            const shareResults = await Promise.all(sharePromises);
            
            // Check if any operation failed
            const anyShareFailed = shareResults.some(result => !result.success);
            if (anyShareFailed) {
              console.warn('Some form sharing operations failed:', shareResults);
            }
            
            // Combine share results
            shareResponse = {
              success: true,
              shared_with: {
                successful: shareResults.flatMap(result => 
                  result.success && result.shared_with ? result.shared_with.successful : []
                ),
                failed: shareResults.flatMap(result => 
                  result.success && result.shared_with ? result.shared_with.failed : []
                )
              }
            };
          }
          
          // Combine all responses for the final result
          quizResponse = {
            success: true,
            quizzes: quizzesResponse.quizzes,
            forms: formsResponse.forms,
            shared_with: shareResponse.shared_with
          };
        } else {
          // For day-based quizzes, follow similar process
          setQuizProgress(20);
          const quizzesResponse = await generateDayQuizzes({
            content: processedContent,
            level: quizConfig.level,
            questionsPerItem: parseInt(quizConfig.questionsPerItem, 10),
            titleTemplate: subject
          });
          
          if (!quizzesResponse.success) {
            throw new Error(quizzesResponse.message || 'Failed to generate day quizzes');
          }
          
          setQuizProgress(50);
          const formsResponse = await createMultipleForms({
            quizDataList: quizzesResponse.quizzes,
            titleTemplate: subject,
            type: 'day'
          });
          
          if (!formsResponse.success) {
            throw new Error(formsResponse.message || 'Failed to create quiz forms');
          }
          
          setQuizProgress(80);
          let shareResponse = { success: true };
          
          if (quizConfig.sendEmails && (quizConfig.emails.length > 0 || quizConfig.trainerEmails.length > 0)) {
            const sharePromises = formsResponse.forms.filter(form => form).map(form => 
              shareQuizForms({
                formId: form.form_id,
                emails: quizConfig.emails,
                trainerEmails: quizConfig.trainerEmails,
                title: form.title,
                editUrl: form.edit_url,
                viewUrl: form.view_url
              })
            );
            
            const shareResults = await Promise.all(sharePromises);
            const anyShareFailed = shareResults.some(result => !result.success);
            
            if (anyShareFailed) {
              console.warn('Some form sharing operations failed:', shareResults);
            }
            
            shareResponse = {
              success: true,
              shared_with: {
                successful: shareResults.flatMap(result => 
                  result.success && result.shared_with ? result.shared_with.successful : []
                ),
                failed: shareResults.flatMap(result => 
                  result.success && result.shared_with ? result.shared_with.failed : []
                )
              }
            };
          }
          
          quizResponse = {
            success: true,
            quizzes: quizzesResponse.quizzes,
            forms: formsResponse.forms,
            shared_with: shareResponse.shared_with
          };
        }
      }
      
      // Clean up and update UI
      clearInterval(progressInterval);
      setQuizProgress(100);
      
      // Small delay to show 100% progress
      setTimeout(() => {
        setQuizResults(quizResponse);
        setStep('success');
      }, 500);
      
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