// src/App.js
import React, { useState } from 'react';
import './App.css';
import Header from './components/Header';
import Footer from './components/Footer';
import StepsIndicator from './components/StepsIndicator';
import Step1Parameters from './components/Step1Parameters';
import Step2Plan from './components/Step2Plan';
import Step3Generation from './components/Step3Generation';
import EditSectionModal from './components/EditSectionModal';
import AddSectionModal from './components/AddSectionModal';
import ErrorModal from './components/ErrorModal';
import LoadingSpinner from './components/LoadingSpinner'; // Import the new component
import { generatePlan, generateContent, generateFiles, getDownloadUrl } from './services/api';

// Import the CSS for the loading spinner
import './components/LoadingSpinner.css';

function App() {
  // State for steps navigation
  const [currentStep, setCurrentStep] = useState(1);
  const [currentEditId, setCurrentEditId] = useState(null);
  
  // State for presentation sections
  const [sections, setSections] = useState([]);
  
  // State for form fields
  const [formData, setFormData] = useState({
    subject: '',
    level: '',
    planType: '',
    description: '',
    format: 'pdf',
    trainerName: ''
  });
  
  // State for API response and errors
  const [apiPlanResponse, setApiPlanResponse] = useState(null);
  const [apiContentResponse, setApiContentResponse] = useState(null);
  const [apiFilesResponse, setApiFilesResponse] = useState(null);
  const [errorMessage, setErrorMessage] = useState('');
  
  // State for modals
  const [showEditModal, setShowEditModal] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  const [showErrorModal, setShowErrorModal] = useState(false);
  
  // State for generation step
  const [isGenerating, setIsGenerating] = useState(false);
  const [generationStep, setGenerationStep] = useState(0); // 0: not started, 1: generating plan, 2: generating content, 3: generating files
  const [generationProgress, setGenerationProgress] = useState(0);
  
  // State for loading spinner
  const [isLoadingPlan, setIsLoadingPlan] = useState(false);
  const [loadingMessage, setLoadingMessage] = useState('');
  
  // Convert API plan response to our sections format
  const convertApiPlanToSections = (apiResponse) => {
    if (!apiResponse || !apiResponse.plan || !apiResponse.plan.sections) {
      return [];
    }
    
    return apiResponse.plan.sections.map((section, index) => ({
      id: index + 1,
      title: section.section,
      subsections: section['sous-sections'] || []
    }));
  };
  
  // Convert our sections to API plan format
  const convertSectionsToApiPlan = () => {
    return {
      titre: formData.subject,
      sections: sections.map(section => ({
        section: section.title,
        'sous-sections': section.subsections
      }))
    };
  };
  
  // Handle API errors
  const handleApiError = (error, step) => {
    console.error(`Error in step ${step}:`, error);
    setErrorMessage(`Error during ${
      step === 1 ? 'plan generation' : 
      step === 2 ? 'content generation' : 
      'file generation'
    }: ${error.message || 'Unknown error'}`);
    setShowErrorModal(true);
    setIsGenerating(false);
    setIsLoadingPlan(false);
    setLoadingMessage('');
  };
  
  // Handle navigation between steps
  const goToStep = async (step) => {
    if (currentStep === 1 && step === 2) {
      // Validate form before proceeding
      if (!formData.subject || !formData.level || !formData.planType) {
        alert('Veuillez remplir tous les champs obligatoires.');
        return;
      }
      
      // If we're moving to step 2, generate a plan if sections are empty
      if (sections.length === 0) {
        try {
          setIsGenerating(true);
          setIsLoadingPlan(true);
          setLoadingMessage(`Génération du plan pour "${formData.subject}" en cours...`);
          setGenerationStep(1);
          setGenerationProgress(25);
          
          console.log('Requesting plan generation with data:', formData);
          const planResponse = await generatePlan(formData);
          
          console.log('Plan response received:', planResponse);
          setApiPlanResponse(planResponse);
          
          if (planResponse.success) {
            const newSections = convertApiPlanToSections(planResponse);
            setSections(newSections);
            setIsGenerating(false);
            setIsLoadingPlan(false);
            setLoadingMessage('');
            setCurrentStep(step);
          } else {
            throw new Error(planResponse.message || 'Plan generation failed');
          }
        } catch (error) {
          console.error('Plan generation error:', error);
          handleApiError(error, 1);
          return;
        }
      } else {
        setCurrentStep(step);
      }
    } else if (currentStep === 2 && step === 3) {
      // If moving from step 2 to 3, generate content and files
      setCurrentStep(step);
      generatePresentationContent();
    } else {
      setCurrentStep(step);
    }
  };
  
  // Generate presentation content and files
  const generatePresentationContent = async () => {
    try {
      setIsGenerating(true);
      setIsLoadingPlan(true);
      setLoadingMessage(`Génération du contenu pour "${formData.subject}" en cours...`);
      setGenerationStep(2);
      setGenerationProgress(50);
      
      // Convert our sections to API plan format
      const apiPlan = convertSectionsToApiPlan();
      
      // Generate content
      const contentParams = {
        subject: formData.subject,
        planType: formData.planType,
        plan: apiPlan
      };
      
      console.log('Requesting content generation with params:', contentParams);
      const contentResponse = await generateContent(contentParams);
      console.log('Content response received:', contentResponse);
      setApiContentResponse(contentResponse);
      
      if (!contentResponse.success) {
        throw new Error(contentResponse.message || 'Content generation failed');
      }
      
      setGenerationStep(3);
      setGenerationProgress(75);
      setLoadingMessage(`Génération des fichiers ${formData.format.toUpperCase()} en cours...`);
      
      // Generate files
      const filesParams = {
        subject: formData.subject,
        content: contentResponse.content,
        format: formData.format,
        trainerName: formData.trainerName || 'Presenter'
      };
      
      console.log('Requesting file generation with params:', filesParams);
      const filesResponse = await generateFiles(filesParams);
      console.log('Files response received:', filesResponse);
      setApiFilesResponse(filesResponse);
      
      if (!filesResponse.success) {
        throw new Error(filesResponse.message || 'File generation failed');
      }
      
      setGenerationProgress(100);
      setIsGenerating(false);
      setIsLoadingPlan(false);
      setLoadingMessage('');
    } catch (error) {
      console.error('Content/file generation error:', error);
      handleApiError(error, generationStep);
    }
  };
  
  // Handle download of generated files
  const handleDownload = (fileInfo) => {
    if (!fileInfo || !fileInfo.download_url) {
      setErrorMessage('No file available for download');
      setShowErrorModal(true);
      return;
    }
    
    const downloadUrl = getDownloadUrl(fileInfo.download_url);
    window.open(downloadUrl, '_blank');
  };
  
  // Open edit modal
  const openEditModal = (id) => {
    setCurrentEditId(id);
    setShowEditModal(true);
  };
  
  // Open add modal
  const openAddModal = () => {
    setShowAddModal(true);
  };
  
  // Save edited section
  const saveSection = (title, subsections) => {
    setSections(sections.map(section => 
      section.id === currentEditId 
        ? { ...section, title, subsections } 
        : section
    ));
    setShowEditModal(false);
  };
  
  // Add new section
  const addNewSection = (title, subsections) => {
    const newId = Math.max(...(sections.length ? sections.map(s => s.id) : [0]), 0) + 1;
    setSections([...sections, { id: newId, title, subsections }]);
    setShowAddModal(false);
  };
  
  // Move section up or down
  const moveSection = (id, direction) => {
    const index = sections.findIndex(s => s.id === id);
    if (index === -1) return;
    
    const newSections = [...sections];
    
    if (direction === 'up' && index > 0) {
      // Move up
      [newSections[index], newSections[index - 1]] = [newSections[index - 1], newSections[index]];
    } else if (direction === 'down' && index < sections.length - 1) {
      // Move down
      [newSections[index], newSections[index + 1]] = [newSections[index + 1], newSections[index]];
    }
    
    setSections(newSections);
  };
  
  // Update form data
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };
  
  // Reset error modal
  const closeErrorModal = () => {
    setShowErrorModal(false);
    setErrorMessage('');
  };
  
  return (
    <div className="app">
      <Header />
      
      <main>
        <div className="container">
          <header className="header-presentation">
            <h1>Présentation BUILDER</h1>
            <p>Créez des présentations professionnelles en quelques clics</p>
          </header>
          
          <StepsIndicator currentStep={currentStep} />
          
          {currentStep === 1 && (
            <Step1Parameters 
              formData={formData} 
              onChange={handleInputChange} 
              onNext={() => goToStep(2)} 
            />
          )}
          
          {currentStep === 2 && (
            <Step2Plan 
              sections={sections} 
              onMoveSection={moveSection} 
              onEditSection={openEditModal} 
              onAddSection={openAddModal}
              onPrevious={() => goToStep(1)} 
              onNext={() => goToStep(3)} 
            />
          )}
          
          {currentStep === 3 && (
            <Step3Generation 
              isGenerating={isGenerating}
              progress={generationProgress}
              filesResponse={apiFilesResponse}
              onDownload={handleDownload}
            />
          )}
          
          {showEditModal && (
            <EditSectionModal 
              section={sections.find(s => s.id === currentEditId)} 
              onClose={() => setShowEditModal(false)} 
              onSave={saveSection} 
            />
          )}
          
          {showAddModal && (
            <AddSectionModal 
              onClose={() => setShowAddModal(false)} 
              onAdd={addNewSection} 
            />
          )}
          
          {showErrorModal && (
            <ErrorModal 
              message={errorMessage}
              onClose={closeErrorModal}
            />
          )}
          
          {/* Popup loading spinner */}
          {isLoadingPlan && <LoadingSpinner message={loadingMessage} />}
        </div>
      </main>
      
      <Footer />
    </div>
  );
}

export default App;