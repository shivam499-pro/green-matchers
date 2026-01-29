
import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import App from './App.jsx';
import Home from './pages/Home.jsx';
import JobSearch from './pages/JobSearch.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Trends from './pages/Trends.jsx';
import CareerPathPage from './pages/CareerPathPage.jsx';
import Login from './pages/LoginPage.jsx';  // ✅ Use your existing LoginPage.jsx
import Register from './pages/Register.jsx';

// NEW BACKEND SHOWCASE PAGES
import CompaniesShowcase from './pages/CompaniesShowcase.jsx';
import LanguagesDemo from './pages/LanguagesDemo.jsx';
import APIDocs from './pages/APIDocs.jsx';
import VectorAIDemo from './pages/VectorAIDemo.jsx';
import { LanguageProvider } from './context/LanguageContext';


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <LanguageProvider> {/* ✅ ADD THIS WRAPPER */}
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<App />}>
            <Route index element={<Home />} />
            <Route path="job-search" element={<JobSearch />} />
            <Route path="dashboard" element={<Dashboard />} />
            <Route path="trends" element={<Trends />} />
            <Route path="career-path" element={<CareerPathPage />} />
            <Route path="login" element={<Login />} />
            <Route path="register" element={<Register />} />
            
            {/* NEW BACKEND SHOWCASE ROUTES */}
            <Route path="companies" element={<CompaniesShowcase />} />
            <Route path="languages" element={<LanguagesDemo />} />
            <Route path="api-docs" element={<APIDocs />} />
            <Route path="vector-ai" element={<VectorAIDemo />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </LanguageProvider> {/* ✅ ADD THIS WRAPPER */}
  </React.StrictMode>
);