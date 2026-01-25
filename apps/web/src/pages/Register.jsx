import React from 'react';
import { Link } from 'react-router-dom';

const Register = () => {
  return (
    <div className="max-w-md mx-auto">
      <div className="glass-effect rounded-2xl p-8 shadow-2xl text-center">
        <div className="w-20 h-20 bg-gradient-to-br from-blue-500 to-purple-500 rounded-2xl flex items-center justify-center mx-auto mb-4 shadow-lg">
          <span className="text-3xl">🚀</span>
        </div>
        <h1 className="text-3xl font-bold text-white mb-4">Registration</h1>
        <p className="text-slate-300 mb-6">
          Registration is currently by invitation only. Please contact admin for access.
        </p>
        <Link 
          to="/login" 
          className="inline-block bg-gradient-to-r from-green-500 to-teal-500 text-white px-6 py-3 rounded-xl font-semibold hover:from-green-600 hover:to-teal-600 transition-all"
        >
          Back to Login
        </Link>
      </div>
    </div>
  );
};

export default Register;