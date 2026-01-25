import React from 'react';

const APIDocs = () => {
  const apiEndpoints = [
    {
      method: 'GET',
      path: '/api/jobs',
      description: 'Get all jobs with filters',
      auth: 'Optional'
    },
    {
      method: 'POST', 
      path: '/api/jobs/vector-search',
      description: 'AI semantic search using vector embeddings',
      auth: 'Optional'
    },
    {
      method: 'GET',
      path: '/api/companies',
      description: 'Get all 51 companies',
      auth: 'No'
    },
    {
      method: 'POST',
      path: '/api/career/recommendations',
      description: 'AI career recommendations based on skills',
      auth: 'Optional'
    },
    {
      method: 'POST',
      path: '/api/translate',
      description: 'Translate text to 10 Indian languages',
      auth: 'No'
    },
    {
      method: 'GET',
      path: '/stats',
      description: 'Get database statistics',
      auth: 'No'
    },
    {
      method: 'POST',
      path: '/api/auth/login',
      description: 'User authentication',
      auth: 'No'
    }
  ];

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white mb-4">
          API Documentation
        </h1>
        <p className="text-slate-300 text-lg mb-6">
          50+ RESTful endpoints powered by FastAPI with MariaDB
        </p>
        
        <a 
          href="http://localhost:8000/docs" 
          target="_blank" 
          rel="noopener noreferrer"
          className="inline-flex items-center gap-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-xl font-semibold hover:from-blue-500 hover:to-purple-500 transition-all shadow-lg"
        >
          <span>📚</span>
          Open Interactive Swagger UI
        </a>
      </div>

      {/* API Endpoints */}
      <div className="glass-premium rounded-2xl p-6">
        <h2 className="text-2xl font-bold text-white mb-6">Core Endpoints</h2>
        
        <div className="space-y-4">
          {apiEndpoints.map((endpoint, index) => (
            <div key={index} className="bg-slate-800/50 rounded-xl p-4 border border-slate-700">
              <div className="flex flex-col md:flex-row md:items-center gap-4">
                <div className="flex items-center gap-3">
                  <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                    endpoint.method === 'GET' ? 'bg-green-500/20 text-green-400' :
                    endpoint.method === 'POST' ? 'bg-blue-500/20 text-blue-400' :
                    'bg-purple-500/20 text-purple-400'
                  }`}>
                    {endpoint.method}
                  </span>
                  <code className="text-white font-mono text-sm bg-slate-900 px-3 py-1 rounded">
                    {endpoint.path}
                  </code>
                </div>
                
                <div className="flex-1">
                  <p className="text-slate-300">{endpoint.description}</p>
                </div>
                
                <div className={`px-3 py-1 rounded-full text-sm font-semibold ${
                  endpoint.auth === 'No' ? 'bg-gray-500/20 text-gray-400' :
                  endpoint.auth === 'Optional' ? 'bg-yellow-500/20 text-yellow-400' :
                  'bg-red-500/20 text-red-400'
                }`}>
                  {endpoint.auth}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Quick Stats */}
      <div className="grid md:grid-cols-3 gap-6 mt-8">
        <div className="glass-premium rounded-2xl p-6 text-center">
          <div className="text-3xl font-bold text-blue-400 mb-2">50+</div>
          <div className="text-slate-300">API Endpoints</div>
        </div>
        <div className="glass-premium rounded-2xl p-6 text-center">
          <div className="text-3xl font-bold text-green-400 mb-2">24/7</div>
          <div className="text-slate-300">Production Ready</div>
        </div>
        <div className="glass-premium rounded-2xl p-6 text-center">
          <div className="text-3xl font-bold text-purple-400 mb-2">FastAPI</div>
          <div className="text-slate-300">High Performance</div>
        </div>
      </div>
    </div>
  );
};

export default APIDocs;