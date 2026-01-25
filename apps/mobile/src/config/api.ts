// API Configuration for Green Matchers Mobile App
// Connects to your existing FastAPI backend

const BASE_URL = 'http://localhost:8081'; // Updated to match backend server port
// For production: const BASE_URL = 'https://your-domain.com';

export const API_ENDPOINTS = {
  // Authentication
  REGISTER: `${BASE_URL}/api/auth/register`,
  LOGIN: `${BASE_URL}/api/auth/login`,

  // Career Services
  CAREER_RECOMMENDATIONS: `${BASE_URL}/api/career/recommendations`,
  CAREER_PATH: `${BASE_URL}/api/career/progression`,

  // Job Services
  JOB_SEARCH: `${BASE_URL}/api/jobs/search`,
  JOB_APPLY: `${BASE_URL}/api/jobs/apply`,
  JOB_APPLICATIONS: `${BASE_URL}/api/users/applications`,

  // Vector AI Services
  VECTOR_JOB_SEARCH: `${BASE_URL}/api/vector/jobs/search`,
  VECTOR_CAREER_RECOMMEND: `${BASE_URL}/api/vector/careers/recommend`,

  // Translation Services
  TRANSLATE: `${BASE_URL}/api/translate`,
  LANGUAGES: `${BASE_URL}/api/languages`,

  // User Services
  USER_PROFILE: `${BASE_URL}/api/users/profile`,
  UPDATE_PROFILE: `${BASE_URL}/api/users/profile`,
  UPLOAD_RESUME: `${BASE_URL}/api/users/upload-resume`,

  // System Services
  HEALTH_CHECK: `${BASE_URL}/health`,
  STATS: `${BASE_URL}/stats`,
};

// API Headers Configuration
export const getHeaders = (token: string | null = null) => {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  return headers;
};

// Error Handling
export const handleApiError = (error: any) => {
  if (error.response) {
    // Server responded with a status other than 2xx
    console.error('API Error Response:', error.response.data);
    console.error('Status:', error.response.status);
    return {
      success: false,
      error: error.response.data.error || 'Server error occurred',
      status: error.response.status,
    };
  } else if (error.request) {
    // Request was made but no response received
    console.error('API Error Request:', error.request);
    return {
      success: false,
      error: 'No response from server. Please check your connection.',
    };
  } else {
    // Something happened in setting up the request
    console.error('API Error:', error.message);
    return {
      success: false,
      error: 'Request setup error: ' + error.message,
    };
  }
};

// API Timeout Configuration
export const API_TIMEOUT = 30000; // 30 seconds

// Supported Languages for the mobile app
export const SUPPORTED_LANGUAGES = [
  { code: 'en', name: 'English', nativeName: 'English' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी' },
  { code: 'bn', name: 'Bengali', nativeName: 'বাংলা' },
  { code: 'te', name: 'Telugu', nativeName: 'తెలుగు' },
  { code: 'ta', name: 'Tamil', nativeName: 'தமிழ்' },
  { code: 'mr', name: 'Marathi', nativeName: 'मराठी' },
  { code: 'gu', name: 'Gujarati', nativeName: 'ગુજરાતી' },
  { code: 'kn', name: 'Kannada', nativeName: 'ಕನ್ನಡ' },
  { code: 'ml', name: 'Malayalam', nativeName: 'മലയാളം' },
  { code: 'or', name: 'Odia', nativeName: 'ଓଡ଼ିଆ' },
];

// Career Categories for filtering
export const CAREER_CATEGORIES = [
  'Renewable Energy',
  'Sustainability',
  'Environmental Science',
  'Green Technology',
  'Carbon Management',
  'ESG Compliance',
  'Clean Energy',
  'Circular Economy',
];

// Job Types
export const JOB_TYPES = [
  'Full-time',
  'Part-time',
  'Contract',
  'Internship',
  'Freelance',
  'Remote',
];

// Experience Levels
export const EXPERIENCE_LEVELS = [
  'Entry Level',
  'Mid Level',
  'Senior Level',
  'Executive',
];