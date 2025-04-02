// src/services/api.js
import axios from 'axios';

// Create an axios instance with a base URL
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Generate presentation plan
export const generatePlan = async (data) => {
  try {
    const response = await api.post('/api/generate-plan', data);
    return response.data;
  } catch (error) {
    console.error('Failed to generate plan:', error);
    throw error;
  }
};

// Generate presentation content and files
export const generateContent = async (data) => {
  try {
    const response = await api.post('/api/generate-content', data);
    return response.data;
  } catch (error) {
    console.error('Failed to generate content:', error);
    throw error;
  }
};

// Generate final files
export const generateFiles = async (data) => {
  try {
    const response = await api.post('/api/generate-files', data);
    return response.data;
  } catch (error) {
    console.error('Failed to generate files:', error);
    throw error;
  }
};

// Helper to construct download URL
export const getDownloadUrl = (filename) => {
  return `${api.defaults.baseURL}/api/download/${filename}`;
};

export default api;