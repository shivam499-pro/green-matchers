import React, { useState } from 'react';
import { useOutletContext } from 'react-router-dom';
import { useLanguage } from '../context/LanguageContext';

const LanguagesDemo = () => {
  const { showToast } = useOutletContext();
  const { currentLanguage, setLanguage, t } = useLanguage();
  const [demoText, setDemoText] = useState('Hello, welcome to our green jobs platform!');
  const [translatedText, setTranslatedText] = useState('');
  const [loading, setLoading] = useState(false);

  const languages = [
    { code: 'en', name: 'English', native: 'English' },
    { code: 'hi', name: 'Hindi', native: 'हिन्दी' },
    { code: 'bn', name: 'Bengali', native: 'বাংলা' },
    { code: 'te', name: 'Telugu', native: 'తెలుగు' },
    { code: 'ta', name: 'Tamil', native: 'தமிழ்' },
    { code: 'mr', name: 'Marathi', native: 'मराठी' },
    { code: 'gu', name: 'Gujarati', native: 'ગુજરાતી' },
    { code: 'kn', name: 'Kannada', native: 'ಕನ್ನಡ' },
    { code: 'ml', name: 'Malayalam', native: 'മലയാളം' },
    { code: 'or', name: 'Odia', native: 'ଓଡ଼ିଆ' }
  ];

  const translateText = async (text, targetLang) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          target_lang: targetLang
        })
      });
      const data = await response.json();
      setTranslatedText(data.translated_text || 'Translation service unavailable');
    } catch (error) {
      console.error('Translation failed:', error);
      setTranslatedText('Translation service unavailable - backend connection required');
    } finally {
      setLoading(false);
    }
  };

  const handleLanguageChange = (langCode) => {
    setLanguage(langCode);
    translateText(demoText, langCode);
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white mb-4">
          10 Indian Languages Support
        </h1>
        <p className="text-slate-300 text-lg">
          Multi-language AI translation powered by your backend
        </p>
      </div>

      {/* Language Selection Grid */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
        {languages.map(lang => (
          <button
            key={lang.code}
            onClick={() => handleLanguageChange(lang.code)}
            className={`p-4 rounded-2xl transition-all duration-300 ${
              currentLanguage === lang.code
                ? 'bg-gradient-to-br from-blue-500 to-purple-600 text-white shadow-lg'
                : 'glass-effect text-slate-300 hover:text-white hover:border-blue-500/50'
            } border-2 ${
              currentLanguage === lang.code ? 'border-blue-500' : 'border-white/10'
            }`}
          >
            <div className="text-2xl mb-2">{getLanguageFlag(lang.code)}</div>
            <div className="font-semibold text-sm">{lang.name}</div>
            <div className="text-xs opacity-80 mt-1">{lang.native}</div>
          </button>
        ))}
      </div>

      {/* Translation Demo */}
      <div className="glass-effect rounded-2xl p-6 mb-8">
        <h3 className="text-xl font-bold text-white mb-4">Live Translation Demo</h3>
        
        <div className="grid md:grid-cols-2 gap-6">
          <div>
            <label className="block text-white font-semibold mb-3">English Text</label>
            <textarea
              value={demoText}
              onChange={(e) => setDemoText(e.target.value)}
              className="w-full h-32 bg-slate-800 border border-slate-600 text-white rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Enter text to translate..."
            />
            <button
              onClick={() => translateText(demoText, currentLanguage)}
              disabled={loading}
              className="mt-3 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors disabled:opacity-50"
            >
              {loading ? 'Translating...' : 'Translate'}
            </button>
          </div>

          <div>
            <label className="block text-white font-semibold mb-3">
              Translation in {languages.find(l => l.code === currentLanguage)?.native}
            </label>
            <div className="w-full h-32 bg-slate-800 border border-slate-600 text-white rounded-xl px-4 py-3">
              {loading ? (
                <div className="flex items-center justify-center h-full">
                  <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-blue-500"></div>
                </div>
              ) : (
                translatedText || 'Translation will appear here...'
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Language Statistics */}
      <div className="grid md:grid-cols-3 gap-6">
        <div className="glass-effect rounded-2xl p-6 text-center">
          <div className="text-3xl font-bold text-green-400 mb-2">10</div>
          <div className="text-slate-300">Languages Supported</div>
        </div>
        <div className="glass-effect rounded-2xl p-6 text-center">
          <div className="text-3xl font-bold text-blue-400 mb-2">1.4B+</div>
          <div className="text-slate-300">People Covered</div>
        </div>
        <div className="glass-effect rounded-2xl p-6 text-center">
          <div className="text-3xl font-bold text-purple-400 mb-2">AI</div>
          <div className="text-slate-300">Real-time Translation</div>
        </div>
      </div>
    </div>
  );
};

// Helper function for language flags
function getLanguageFlag(code) {
  const flags = {
    en: '🇺🇸',
    hi: '🇮🇳',
    bn: '🇧🇩',
    te: '🇮🇳',
    ta: '🇮🇳',
    mr: '🇮🇳',
    gu: '🇮🇳',
    kn: '🇮🇳',
    ml: '🇮🇳',
    or: '🇮🇳'
  };
  return flags[code] || '🌐';
}

export default LanguagesDemo;