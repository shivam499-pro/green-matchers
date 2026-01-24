import React, { useState } from 'react';
import { useOutletContext } from 'react-router-dom';

const VectorAIDemo = () => {
  const { showToast } = useOutletContext();
  const [searchQuery, setSearchQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchType, setSearchType] = useState('semantic');

  const demoQueries = [
    "renewable energy engineering",
    "sustainability data analysis", 
    "solar power project management",
    "ESG reporting and compliance",
    "wind energy technology"
  ];

  const performVectorSearch = async () => {
    if (!searchQuery.trim()) return;
    
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/api/jobs/vector-search', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: searchQuery,
          search_type: searchType,
          top_k: 5
        })
      });
      const data = await response.json();
      setResults(data.results || []);
      showToast(`Found ${data.results?.length || 0} matches using Vector AI`, 'success');
    } catch (error) {
      console.error('Vector search failed:', error);
      // Fallback demo results
      setResults([
        {
          job_id: 1,
          title: 'Senior Solar Energy Engineer',
          company: 'Tata Power Renewables',
          similarity_score: 0.92,
          match_reason: 'High semantic match with renewable energy and engineering'
        },
        {
          job_id: 2,
          title: 'Sustainability Data Analyst', 
          company: 'Adani Green Energy',
          similarity_score: 0.88,
          match_reason: 'Strong match with sustainability and data analysis'
        }
      ]);
      showToast('Using demo data - Vector AI backend required', 'warning');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white mb-4">
          MariaDB Vector AI Search
        </h1>
        <p className="text-slate-300 text-lg">
          Semantic search across 48 careers and 24 jobs using vector embeddings
        </p>
      </div>

      {/* Search Section */}
      <div className="glass-premium rounded-2xl p-6 mb-8">
        <div className="flex flex-col md:flex-row gap-4 mb-6">
          <div className="flex-1">
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Describe your ideal job in natural language..."
              className="w-full bg-slate-800 border border-slate-600 text-white rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <button
            onClick={performVectorSearch}
            disabled={loading}
            className="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-6 py-3 rounded-xl font-semibold hover:from-purple-500 hover:to-pink-500 transition-all disabled:opacity-50"
          >
            {loading ? '🔍 AI Searching...' : '🤖 Vector Search'}
          </button>
        </div>

        <div className="flex gap-4 mb-4">
          <label className="flex items-center">
            <input
              type="radio"
              value="semantic"
              checked={searchType === 'semantic'}
              onChange={(e) => setSearchType(e.target.value)}
              className="mr-2"
            />
            <span className="text-white">Semantic Search</span>
          </label>
          <label className="flex items-center">
            <input
              type="radio"
              value="hybrid"
              checked={searchType === 'hybrid'}
              onChange={(e) => setSearchType(e.target.value)}
              className="mr-2"
            />
            <span className="text-white">Hybrid Search</span>
          </label>
        </div>

        {/* Demo Queries */}
        <div className="flex flex-wrap gap-2">
          <span className="text-slate-400 text-sm">Try:</span>
          {demoQueries.map((query, index) => (
            <button
              key={index}
              onClick={() => setSearchQuery(query)}
              className="text-blue-400 hover:text-blue-300 text-sm bg-blue-500/10 hover:bg-blue-500/20 px-3 py-1 rounded-lg transition-colors"
            >
              {query}
            </button>
          ))}
        </div>
      </div>

      {/* Results */}
      <div className="space-y-4">
        {results.map((result, index) => (
          <div key={index} className="glass-premium rounded-2xl p-6 border border-purple-500/30">
            <div className="flex justify-between items-start mb-3">
              <div>
                <h3 className="text-xl font-bold text-white mb-1">{result.title}</h3>
                <p className="text-slate-300">{result.company}</p>
              </div>
              <div className="bg-purple-500/20 text-purple-400 px-3 py-1 rounded-full text-sm font-semibold">
                {(result.similarity_score * 100).toFixed(0)}% Match
              </div>
            </div>
            
            <p className="text-slate-400 text-sm mb-4">{result.match_reason}</p>
            
            <div className="flex justify-between items-center">
              <span className="text-green-400 font-semibold">AI Recommended</span>
              <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors">
                View Job
              </button>
            </div>
          </div>
        ))}
      </div>

      {results.length === 0 && !loading && (
        <div className="text-center py-12">
          <div className="text-6xl mb-4">🤖</div>
          <h3 className="text-xl font-bold text-white mb-2">Vector AI Search Ready</h3>
          <p className="text-slate-400">Enter a job description to find semantic matches using MariaDB Vector AI</p>
        </div>
      )}
    </div>
  );
};

export default VectorAIDemo;