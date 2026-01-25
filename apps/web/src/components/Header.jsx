import React from 'react';
import { Link } from 'react-router-dom';

const Header = ({ currentLanguage, setLanguage }) => {
  const languages = [
    { code: 'en', name: 'English' },
    { code: 'hi', name: 'हिन्दी' },
    { code: 'bn', name: 'বাংলা' },
    { code: 'te', name: 'తెలుగు' },
    { code: 'ta', name: 'தமிழ்' },
    { code: 'mr', name: 'मराठी' },
    { code: 'gu', name: 'ગુજરાતી' },
    { code: 'kn', name: 'ಕನ್ನಡ' },
    { code: 'ml', name: 'മലയാളം' },
    { code: 'or', name: 'ଓଡ଼ିଆ' }
  ];

  return (
    <header className="bg-green-800 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex justify-between items-center">
          <Link to="/" className="flex items-center space-x-2">
            <span className="text-2xl">🌱</span>
            <h1 className="text-2xl font-bold">Green Matchers</h1>
          </Link>
          
          <nav className="flex items-center space-x-6">
            <Link to="/" className="hover:text-green-200">Home</Link>
            <Link to="/careers" className="hover:text-green-200">Careers</Link>
            <Link to="/jobs" className="hover:text-green-200">Jobs</Link>
            <Link to="/languages" className="hover:text-green-200">Languages</Link>
            <Link to="/api-docs" className="hover:text-green-200">API Docs</Link>
            
            <select 
              value={currentLanguage}
              onChange={(e) => setLanguage(e.target.value)}
              className="bg-green-700 text-white px-3 py-1 rounded border border-green-600"
            >
              {languages.map(lang => (
                <option key={lang.code} value={lang.code}>
                  {lang.name}
                </option>
              ))}
            </select>
          </nav>
        </div>
      </div>
    </header>
  );
};

export default Header;