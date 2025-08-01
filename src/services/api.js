// src/services/api.js
const API_BASE_URL = 'http://localhost:5000'; // Change this to your backend URL

/**
 * Generate a presentation plan based on input parameters
 * @param {Object} params - Parameters for plan generation
 * @returns {Promise} - The generated plan
 */
export const generatePlan = async (params) => {
  try {
    console.log('Sending plan request to:', `${API_BASE_URL}/api/generate-plan`);
    console.log('With parameters:', {
      domaine: params.planType,
      sujet: params.subject,
      description_sujet: params.description,
      niveau_apprenant: params.level
    });
    
    const response = await fetch(`${API_BASE_URL}/api/generate-plan`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        domaine: params.planType,
        sujet: params.subject,
        description_sujet: params.description,
        niveau_apprenant: params.level
      }),
    });

    if (!response.ok) {
      console.error('Response not OK:', response.status, response.statusText);
      const errorText = await response.text();
      console.error('Error text:', errorText);
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }
    
    const data = await response.json();
    console.log('Response data:', data);
    return data;
  } catch (error) {
    console.error('Error details:', error);
    throw error;
  }
};

/**
 * Generate a presentation plan organized by days
 * @param {Object} params - Parameters for plan generation
 * @returns {Promise} - The generated day-based plan
 */
export const generatePlanJour = async (params) => {
  try {
    console.log('Sending plan jour request to:', `${API_BASE_URL}/api/generate-plan-jour`);
    console.log('With parameters:', {
      domaine: params.planType,
      sujet: params.subject,
      description_sujet: params.description,
      niveau_apprenant: params.level,
      nombre_jours: params.nombre_jours
    });
    
    const response = await fetch(`${API_BASE_URL}/api/generate-plan-jour`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        domaine: params.planType,
        sujet: params.subject,
        description_sujet: params.description,
        niveau_apprenant: params.level,
        nombre_jours: params.nombre_jours
      }),
    });

    if (!response.ok) {
      console.error('Response not OK:', response.status, response.statusText);
      const errorText = await response.text();
      console.error('Error text:', errorText);
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }
    
    const data = await response.json();
    console.log('Response data:', data);
    return data;
  } catch (error) {
    console.error('Error details:', error);
    throw error;
  }
};

/**
 * Generate detailed content based on the plan
 * @param {Object} params - Parameters including the plan
 * @returns {Promise} - The generated content
 */
export const generateContent = async (params) => {
  try {
    console.log('Sending content request to:', `${API_BASE_URL}/api/generate-content`);
    console.log('With parameters:', {
      domaine: params.planType,
      sujet: params.subject,
      plan: params.plan
    });
    
    const response = await fetch(`${API_BASE_URL}/api/generate-content`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        domaine: params.planType,
        sujet: params.subject,
        plan: params.plan
      }),
    });

    if (!response.ok) {
      console.error('Response not OK:', response.status, response.statusText);
      const errorText = await response.text();
      console.error('Error text:', errorText);
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }
    
    const data = await response.json();
    console.log('Response data:', data);
    return data;
  } catch (error) {
    console.error('Error generating content:', error);
    throw error;
  }
};

/**
 * Generate detailed content based on a day-based plan
 * @param {Object} params - Parameters including the day plan
 * @returns {Promise} - The generated day-based content
 */
export const generateContentJour = async (params) => {
  try {
    console.log('Sending content jour request to:', `${API_BASE_URL}/api/generate-content-jour`);
    console.log('With parameters:', {
      domaine: params.planType,
      sujet: params.subject,
      plan_jour: params.plan
    });
    
    const response = await fetch(`${API_BASE_URL}/api/generate-content-jour`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        domaine: params.planType,
        sujet: params.subject,
        plan_jour: params.plan
      }),
    });

    if (!response.ok) {
      console.error('Response not OK:', response.status, response.statusText);
      const errorText = await response.text();
      console.error('Error text:', errorText);
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }
    
    const data = await response.json();
    console.log('Response data:', data);
    return data;
  } catch (error) {
    console.error('Error generating day-based content:', error);
    throw error;
  }
};

/**
 * Generate presentation files (PDF/PPTX)
 * @param {Object} params - Parameters for file generation
 * @returns {Promise} - Information about the generated files
 */
export const generateFiles = async (params) => {
  try {
    console.log('Sending files request to:', `${API_BASE_URL}/api/generate-files`);
    console.log('With parameters:', {
      sujet: params.subject,
      format: params.format,
      trainer_name: params.trainerName,
      is_day_format: params.isDayFormat
    });
    
    // Determine the endpoint to use based on the format
    const endpoint = params.isDayFormat ? 
      `${API_BASE_URL}/api/generate-files-jour` : 
      `${API_BASE_URL}/api/generate-files`;
    
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        sujet: params.subject,
        contenu: params.content,
        format: params.format === 'pdf' ? 'pdf' : params.format === 'pptx' ? 'pptx' : 'both',
        trainer_name: params.trainerName || 'Presenter'
      }),
    });

    if (!response.ok) {
      console.error('Response not OK:', response.status, response.statusText);
      const errorText = await response.text();
      console.error('Error text:', errorText);
      throw new Error(`HTTP error! status: ${response.status}, message: ${errorText}`);
    }
    
    const data = await response.json();
    console.log('Response data:', data);
    return data;
  } catch (error) {
    console.error('Error generating files:', error);
    throw error;
  }
};

/**
 * Get the full download URL for a file
 * @param {string} relativeUrl - The relative URL from the API
 * @returns {string} - The full URL for downloading
 */
export const getDownloadUrl = (relativeUrl) => {
  if (!relativeUrl) return '';
  if (relativeUrl.startsWith('http')) return relativeUrl;
  return `${API_BASE_URL}${relativeUrl}`;
};