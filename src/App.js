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

function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [currentEditId, setCurrentEditId] = useState(null);
  const [sections, setSections] = useState([
    {
      id: 1,
      title: "Introduction Python",
      subsections: ["Définition Python", "Avantages Python", "Domaine d'application Python"]
    },
    {
      id: 2,
      title: "Installation et configuration",
      subsections: ["Téléchargement et installation", "Configuration de l'environnement", "Premier programme \"Hello World\""]
    },
    {
      id: 3,
      title: "Syntaxe de base",
      subsections: ["Variables et types de données", "Opérateurs", "Structures conditionnelles"]
    }
  ]);
  
  // State for form fields
  const [formData, setFormData] = useState({
    subject: '',
    level: '',
    planType: '',
    description: '',
    format: 'pdf'
  });
  
  // State for modals
  const [showEditModal, setShowEditModal] = useState(false);
  const [showAddModal, setShowAddModal] = useState(false);
  
  // State for generation step
  const [isGenerating, setIsGenerating] = useState(true);
  
  // Handle navigation between steps
  const goToStep = (step) => {
    if (currentStep === 1 && step === 2) {
      // Validate form before proceeding
      if (!formData.subject || !formData.level || !formData.planType) {
        alert('Veuillez remplir tous les champs obligatoires.');
        return;
      }
    }
    
    setCurrentStep(step);
    
    // If moving to step 3, simulate loading
    if (step === 3) {
      setIsGenerating(true);
      setTimeout(() => {
        setIsGenerating(false);
      }, 3000);
    }
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
    const newId = Math.max(...sections.map(s => s.id), 0) + 1;
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
        </div>
      </main>
      
      <Footer />
    </div>
  );
}

export default App;