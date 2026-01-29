import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
  headers: { 'Content-Type': 'application/json' },
});

export const login = async (username, password) => {
  const response = await api.post('/auth/login', {
    username,
    password,
  });
  return response.data;
};

export const register = async (userData) => {
  const response = await api.post('/auth/register', userData);
  return response.data;
};

export const getJobTrends = async () => {
  const response = await api.get('/system/job-trends');
  return response.data;
};

export const matchJobs = async (token, skills, location) => {
  const response = await api.post('/vector/match-jobs', {
    skill_text: skills,
    lang: 'en',
    location,
  }, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const saveJob = async (token, jobId) => {
  const response = await api.post(`/users/save-job?job_id=${jobId}`, {}, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const generateResume = async (token, skills, location) => {
  const response = await api.post('/vector/generate-resume', {
    skill_text: skills,
    lang: 'en',
    location,
  }, {
    headers: { Authorization: `Bearer ${token}` },
    responseType: 'blob',
  });
  return response.data;
};

export const getSkillsTrends = async () => {
  const response = await api.get('/system/trends/skills');
  return response.data;
};

export const getCompaniesTrends = async () => {
  const response = await api.get('/system/trends/companies');
  return response.data;
};