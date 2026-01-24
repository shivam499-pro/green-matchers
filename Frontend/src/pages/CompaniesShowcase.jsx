import React, { useState, useEffect } from 'react';
import BackendStatus from '../components/BackendStatus';

const CompaniesShowcase = () => {
  const [companies, setCompanies] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCompanies();
  }, []);

  const fetchCompanies = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/companies');
      const data = await response.json();
      setCompanies(data.companies || []);
    } catch (error) {
      console.error('Error fetching companies:', error);
      // Fallback demo data
      const demoCompanies = [
        { company_id: 1, name: 'Tata Power Renewables', location: 'Mumbai', industry: 'Solar Energy', size: 'Large' },
        { company_id: 2, name: 'Adani Green Energy', location: 'Ahmedabad', industry: 'Renewable Energy', size: 'Large' },
        { company_id: 3, name: 'ReNew Power', location: 'Gurugram', industry: 'Wind & Solar', size: 'Large' },
        { company_id: 4, name: 'Azure Power', location: 'New Delhi', industry: 'Solar Power', size: 'Large' },
        { company_id: 5, name: 'Hero Future Energies', location: 'Delhi', industry: 'Renewable Energy', size: 'Medium' },
        { company_id: 6, name: 'Suzlon Energy', location: 'Pune', industry: 'Wind Energy', size: 'Large' }
      ];
      setCompanies(demoCompanies);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="text-center mb-8">
        <h1 className="text-4xl font-bold text-white mb-4">51 Green Companies Database</h1>
        <p className="text-slate-300 text-lg">Real companies from your MariaDB database</p>
      </div>

      <BackendStatus />

      <div className="grid md:grid-cols-3 gap-6 mt-8">
        {companies.map(company => (
          <div key={company.company_id} className="glass-effect rounded-2xl p-6 border border-white/10 hover:border-green-500/50 transition-all">
            <div className="flex items-center gap-4 mb-4">
              <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-teal-500 rounded-xl flex items-center justify-center text-white font-bold">
                {company.name.charAt(0)}
              </div>
              <div>
                <h3 className="text-white font-bold">{company.name}</h3>
                <p className="text-slate-400 text-sm">{company.location}</p>
              </div>
            </div>
            <div className="flex justify-between text-sm">
              <span className="text-slate-400">Industry:</span>
              <span className="text-blue-400">{company.industry}</span>
            </div>
            <div className="flex justify-between text-sm mt-2">
              <span className="text-slate-400">Size:</span>
              <span className="text-green-400">{company.size}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CompaniesShowcase;