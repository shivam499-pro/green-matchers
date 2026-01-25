import { useState, useEffect } from 'react';
import { Outlet, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { LanguageProvider } from './context/LanguageContext';
import { ThemeProvider } from './context/ThemeContext';
import Navbar from './components/Navbar';
import LoadingSpinner from './components/LoadingSpinner';
import Toast from './components/Toast';
import ParticleBackground from './components/ParticleBackground';

function AppContent() {
  const [loading, setLoading] = useState(true);
  const [toast, setToast] = useState(null);
  const { user, login } = useAuth();
  const location = useLocation();

  // Initialize user from localStorage
  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (token && userData) {
      try {
        login(JSON.parse(userData));
      } catch (error) {
        console.error('Error parsing user data:', error);
        localStorage.removeItem('user');
        localStorage.removeItem('token');
      }
    }
    
    const timer = setTimeout(() => setLoading(false), 800);
    return () => clearTimeout(timer);
  }, [login]);

  // Scroll reveal observer
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
          }
        });
      },
      { 
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      }
    );
    
    const elements = document.querySelectorAll('.scroll-reveal, .reveal');
    elements.forEach((el) => observer.observe(el));
    
    return () => observer.disconnect();
  }, [location.pathname]);

  // Toast notification function
  const showToast = (message, type = 'info') => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3000);
  };

  // Loading screen
  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 relative overflow-hidden transition-colors duration-500">
      {/* Enhanced Background Animation - ALWAYS BEHIND EVERYTHING */}
      {location.pathname === '/' && (
        <div className="absolute inset-0 z-0">
          <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-blue-500/5 via-transparent to-purple-500/5 animate-pulse"></div>
          <div className="absolute top-20 right-20 w-96 h-96 bg-gradient-to-br from-cyan-400/10 to-teal-400/10 rounded-full blur-3xl animate-float"></div>
          <div className="absolute bottom-20 left-20 w-96 h-96 bg-gradient-to-br from-emerald-400/10 to-green-400/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }}></div>
          <div className="absolute top-1/2 right-1/3 w-64 h-64 bg-gradient-to-br from-purple-400/10 to-pink-400/10 rounded-full blur-2xl animate-float" style={{ animationDelay: '1s' }}></div>
          
          {/* Floating Particles */}
          <div className="absolute inset-0 pointer-events-none">
            <div className="absolute top-10 left-10 w-2 h-2 bg-blue-400/30 rounded-full animate-ping" style={{ animationDuration: '3s' }}></div>
            <div className="absolute top-40 right-40 w-1 h-1 bg-cyan-400/30 rounded-full animate-ping" style={{ animationDuration: '4s', animationDelay: '1s' }}></div>
            <div className="absolute bottom-40 left-1/3 w-1.5 h-1.5 bg-emerald-400/30 rounded-full animate-ping" style={{ animationDuration: '5s', animationDelay: '2s' }}></div>
          </div>
        </div>
      )}
      
      {/* Navigation - Fixed at top */}
      <div className="relative z-50">
        <Navbar />
      </div>

      {/* Main Content Wrapper - Enhanced with better spacing and layout */}
      <main className="relative z-10 min-h-screen">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="min-h-[calc(100vh-200px)]">
            <Outlet context={{ showToast, user }} />
          </div>
        </div>
      </main>

      {/* Toast Notifications */}
      {toast && (
        <div className="fixed bottom-6 right-6 z-50">
          <Toast 
            message={toast.message} 
            type={toast.type} 
            onClose={() => setToast(null)}
          />
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <ThemeProvider>
      <LanguageProvider>
        <AuthProvider>
          <AppContent />
        </AuthProvider>
      </LanguageProvider>
    </ThemeProvider>
  );
}

export default App;