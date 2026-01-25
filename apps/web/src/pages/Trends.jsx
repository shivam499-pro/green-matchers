import { useState, useEffect } from 'react';
import { getJobTrends, getSkillsTrends, getCompaniesTrends } from '../utils/api';

const Trends = () => {
  const [activeTab, setActiveTab] = useState('demand');
  const [trends, setTrends] = useState({
    labels: [],
    data: []
  });
  const [skillsData, setSkillsData] = useState([]);
  const [companiesData, setCompaniesData] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedTimeframe, setSelectedTimeframe] = useState('month');

  useEffect(() => {
    const fetchAllTrends = async () => {
      try {
        // Fetch job trends (city demand)
        const trendsData = await getJobTrends();
        setTrends({
          labels: trendsData.chart.data.labels,
          data: trendsData.chart.data.datasets[0].data
        });

        // Fetch skills trends
        const skillsResponse = await getSkillsTrends();
        setSkillsData(skillsResponse.skills);

        // Fetch companies trends  
        const companiesResponse = await getCompaniesTrends();
        setCompaniesData(companiesResponse.companies);

      } catch (error) {
        console.error('Failed to fetch trends:', error);
        // Fallback to mock data
        setTrends({
          labels: ['Bengaluru', 'Mumbai', 'Delhi NCR', 'Pune', 'Hyderabad', 'Chennai'],
          data: [18, 15, 12, 8, 7, 6]
        });
        setSkillsData([
          { name: 'Solar PV Design', demand: 95, growth: '+25%', jobs: 145 },
          { name: 'Carbon Accounting', demand: 92, growth: '+30%', jobs: 128 },
          { name: 'ESG Reporting', demand: 88, growth: '+22%', jobs: 156 },
          { name: 'Renewable Analytics', demand: 85, growth: '+20%', jobs: 112 },
          { name: 'Green Building (LEED)', demand: 82, growth: '+18%', jobs: 98 },
          { name: 'Wind Energy Systems', demand: 78, growth: '+15%', jobs: 87 }
        ]);
        setCompaniesData([
          { name: 'Tata Power Renewables', openings: 47, growth: '+35%', rating: 4.5 },
          { name: 'Adani Green Energy', openings: 38, growth: '+28%', rating: 4.3 },
          { name: 'ReNew Power', openings: 32, growth: '+22%', rating: 4.4 },
          { name: 'Suzlon Energy', openings: 28, growth: '+18%', rating: 4.2 },
          { name: 'Azure Power', openings: 24, growth: '+30%', rating: 4.3 },
          { name: 'Hero Future Energies', openings: 19, growth: '+25%', rating: 4.1 }
        ]);
      } finally {
        setIsLoading(false);
      }
    };
    
    fetchAllTrends();
  }, []);

  const tabs = [
    { id: 'demand', label: 'Job Demand', icon: '📊' },
    { id: 'skills', label: 'Hot Skills', icon: '🔥' },
    { id: 'companies', label: 'Top Companies', icon: '🏆' },
    { id: 'salary', label: 'Salary Trends', icon: '💰' }
  ];

  const salaryData = [
    { role: 'Solar Engineer', avg: '₹16L', growth: '+12%', demand: 'High' },
    { role: 'ESG Analyst', avg: '₹14L', growth: '+15%', demand: 'Very High' },
    { role: 'Sustainability Manager', avg: '₹20L', growth: '+10%', demand: 'High' },
    { role: 'Green Architect', avg: '₹18L', growth: '+8%', demand: 'Medium' },
    { role: 'Carbon Analyst', avg: '₹15L', growth: '+18%', demand: 'Very High' }
  ];

  const growthAreas = [
    { area: 'Electric Vehicles', growth: '+45%', jobs: 234, color: 'from-blue-500 to-blue-600' },
    { area: 'Green Hydrogen', growth: '+52%', jobs: 189, color: 'from-purple-500 to-purple-600' },
    { area: 'Carbon Capture', growth: '+38%', jobs: 156, color: 'from-teal-500 to-teal-600' },
    { area: 'Smart Grids', growth: '+41%', jobs: 201, color: 'from-green-500 to-green-600' },
    { area: 'Waste to Energy', growth: '+35%', jobs: 145, color: 'from-orange-500 to-orange-600' },
    { area: 'Sustainable Agriculture', growth: '+29%', jobs: 123, color: 'from-lime-500 to-lime-600' }
  ];

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 relative overflow-hidden">
        {/* Enhanced Background Animation */}
        <div className="absolute inset-0">
          <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-blue-500/5 via-transparent to-purple-500/5 animate-pulse"></div>
          <div className="absolute top-20 right-20 w-96 h-96 bg-gradient-to-br from-cyan-400/10 to-teal-400/10 rounded-full blur-3xl animate-float"></div>
          <div className="absolute bottom-20 left-20 w-96 h-96 bg-gradient-to-br from-emerald-400/10 to-green-400/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }}></div>
        </div>

        <div className="flex justify-center items-center py-20 relative z-10">
          <div className="relative group">
            <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin group-hover:scale-110 transition-transform"></div>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-2xl group-hover:scale-110 transition-transform">📊</span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 relative overflow-hidden">
      {/* Enhanced Background Animation */}
      <div className="absolute inset-0">
        <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-blue-500/5 via-transparent to-purple-500/5 animate-pulse"></div>
        <div className="absolute top-20 right-20 w-96 h-96 bg-gradient-to-br from-cyan-400/10 to-teal-400/10 rounded-full blur-3xl animate-float"></div>
        <div className="absolute bottom-20 left-20 w-96 h-96 bg-gradient-to-br from-emerald-400/10 to-green-400/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }}></div>
      </div>

      <div className="relative z-10 w-full max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="text-4xl font-extrabold text-white mb-4 tracking-tight bg-gradient-to-r from-blue-400 via-teal-400 to-purple-400 bg-clip-text text-transparent animate-gradient">
            Market Intelligence
          </h1>
          <p className="text-slate-300 text-lg text-opacity-90">
            Real-time insights powered by MariaDB analytics
          </p>
        </div>

        {/* Timeframe Selector */}
        <div className="flex justify-center gap-3 flex-wrap">
          {['week', 'month', 'quarter', 'year'].map((timeframe) => (
            <button
              key={timeframe}
              onClick={() => setSelectedTimeframe(timeframe)}
              className={`group relative px-6 py-3 rounded-xl font-semibold transition-all ${
                selectedTimeframe === timeframe
                  ? 'bg-gradient-to-r from-blue-600 to-teal-600 text-white shadow-xl hover:shadow-2xl transform hover:scale-105 border border-blue-400/30'
                  : 'bg-slate-800/50 text-slate-300 hover:bg-slate-700/50 border border-slate-600/50 backdrop-blur-sm'
              }`}
            >
              <span className="relative z-10">
                {timeframe.charAt(0).toUpperCase() + timeframe.slice(1)}
              </span>
              {selectedTimeframe === timeframe && (
                <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
              )}
            </button>
          ))}
        </div>

        {/* Tab Navigation */}
        <div className="glass-ultra rounded-3xl p-3 border border-white/20 shadow-2xl shadow-blue-500/10">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`group relative px-6 py-4 rounded-xl font-bold transition-all ${
                  activeTab === tab.id
                    ? 'bg-gradient-to-r from-blue-600 to-teal-600 text-white shadow-xl hover:shadow-2xl transform hover:scale-105 border border-blue-400/30'
                    : 'text-slate-300 hover:bg-slate-800/50 border border-slate-600/50 backdrop-blur-sm'
                }`}
              >
                <span className="relative z-10 flex items-center justify-center gap-3">
                  <span className="text-xl">{tab.icon}</span>
                  <span className="hidden sm:inline">{tab.label}</span>
                </span>
                {activeTab === tab.id && (
                  <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Content based on active tab */}
        {activeTab === 'demand' && (
          <div className="space-y-6">
            {/* City Demand Chart */}
            <div className="glass-ultra rounded-3xl p-6 border border-white/20 shadow-2xl shadow-blue-500/10">
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
                <span className="text-2xl">📍</span> Job Demand by City
              </h2>
              <div className="space-y-4">
                {trends.labels.map((label, index) => (
                  <div key={index} className="group relative glass-premium rounded-xl p-4 hover:shadow-2xl hover:shadow-blue-500/20 transition-all duration-500 hover:-translate-y-1 cursor-pointer border border-white/10 overflow-hidden hover:border-blue-400/30">
                    {/* Animated background gradient */}
                    <div className="absolute inset-0 bg-gradient-to-br from-blue-500/0 via-teal-500/0 to-purple-500/0 group-hover:from-blue-500/10 group-hover:via-teal-500/10 group-hover:to-purple-500/10 transition-all duration-500"></div>
                    
                    <div className="relative z-10">
                      <div className="flex items-center justify-between mb-3">
                        <div className="flex items-center gap-4">
                          <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-teal-500 rounded-xl flex items-center justify-center text-white font-bold shadow-lg shadow-blue-500/20 group-hover:scale-110 transition-transform duration-500">
                            {index + 1}
                          </div>
                          <span className="text-white font-bold text-lg group-hover:text-blue-400 transition-colors">
                            {label}
                          </span>
                        </div>
                        <span className="bg-gradient-to-r from-green-500 to-emerald-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-lg shadow-green-500/20 group-hover:scale-105 transition-transform">
                          {trends.data[index]}% Share
                        </span>
                      </div>
                      <div className="w-full bg-slate-800/50 rounded-full h-4 border border-slate-600/50 overflow-hidden">
                        <div 
                          className="bg-gradient-to-r from-blue-500 to-teal-500 h-4 rounded-full transition-all duration-1000 ease-out shadow-lg shadow-blue-500/30"
                          style={{ width: `${(trends.data[index] / 20) * 100}%` }}
                        ></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Key Metrics */}
            <div className="grid md:grid-cols-3 gap-6">
              <div className="group relative glass-premium rounded-2xl p-6 text-center hover:shadow-2xl hover:shadow-blue-500/20 transition-all duration-500 hover:-translate-y-2 cursor-pointer border border-white/10 overflow-hidden hover:border-blue-400/30">
                {/* Animated background gradient */}
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500/0 via-teal-500/0 to-purple-500/0 group-hover:from-blue-500/10 group-hover:via-teal-500/10 group-hover:to-purple-500/10 transition-all duration-500"></div>
                
                <div className="relative z-10">
                  <div className="text-5xl mb-4 group-hover:scale-110 transition-transform duration-500">📈</div>
                  <div className="text-4xl font-extrabold text-blue-400 mb-3 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-blue-400 group-hover:to-teal-400 group-hover:bg-clip-text transition-all duration-500">
                    +32%
                  </div>
                  <div className="text-slate-300 text-lg font-medium tracking-wide">Market Growth</div>
                </div>
              </div>
              <div className="group relative glass-premium rounded-2xl p-6 text-center hover:shadow-2xl hover:shadow-blue-500/20 transition-all duration-500 hover:-translate-y-2 cursor-pointer border border-white/10 overflow-hidden hover:border-blue-400/30">
                {/* Animated background gradient */}
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500/0 via-teal-500/0 to-purple-500/0 group-hover:from-blue-500/10 group-hover:via-teal-500/10 group-hover:to-purple-500/10 transition-all duration-500"></div>
                
                <div className="relative z-10">
                  <div className="text-5xl mb-4 group-hover:scale-110 transition-transform duration-500">💼</div>
                  <div className="text-4xl font-extrabold text-teal-400 mb-3 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-teal-400 group-hover:to-blue-400 group-hover:bg-clip-text transition-all duration-500">
                    547
                  </div>
                  <div className="text-slate-300 text-lg font-medium tracking-wide">Active Jobs</div>
                </div>
              </div>
              <div className="group relative glass-premium rounded-2xl p-6 text-center hover:shadow-2xl hover:shadow-blue-500/20 transition-all duration-500 hover:-translate-y-2 cursor-pointer border border-white/10 overflow-hidden hover:border-blue-400/30">
                {/* Animated background gradient */}
                <div className="absolute inset-0 bg-gradient-to-br from-blue-500/0 via-teal-500/0 to-purple-500/0 group-hover:from-blue-500/10 group-hover:via-teal-500/10 group-hover:to-purple-500/10 transition-all duration-500"></div>
                
                <div className="relative z-10">
                  <div className="text-5xl mb-4 group-hover:scale-110 transition-transform duration-500">🏢</div>
                  <div className="text-4xl font-extrabold text-purple-400 mb-3 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-purple-400 group-hover:to-pink-400 group-hover:bg-clip-text transition-all duration-500">
                    52
                  </div>
                  <div className="text-slate-300 text-lg font-medium tracking-wide">Hiring Companies</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'skills' && (
          <div className="space-y-6">
            <div className="glass-ultra rounded-3xl p-6 border border-white/20 shadow-2xl shadow-blue-500/10">
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
                <span className="text-2xl">🔥</span> Most In-Demand Skills
              </h2>
              <div className="space-y-4">
                {skillsData.map((skill, index) => (
                  <div key={index} className="group relative glass-premium rounded-xl p-5 hover:shadow-2xl hover:shadow-blue-500/20 transition-all duration-500 hover:-translate-y-1 cursor-pointer border border-white/10 overflow-hidden hover:border-blue-400/30">
                    {/* Animated background gradient */}
                    <div className="absolute inset-0 bg-gradient-to-br from-blue-500/0 via-teal-500/0 to-purple-500/0 group-hover:from-blue-500/10 group-hover:via-teal-500/10 group-hover:to-purple-500/10 transition-all duration-500"></div>
                    
                    <div className="relative z-10">
                      <div className="flex items-center justify-between mb-4">
                        <h3 className="text-lg font-bold text-white group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-blue-400 group-hover:to-teal-400 group-hover:bg-clip-text transition-all duration-500">
                          {skill.name}
                        </h3>
                        <div className="flex items-center gap-3">
                          <span className="bg-gradient-to-r from-green-500 to-emerald-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-lg shadow-green-500/20 group-hover:scale-105 transition-transform">
                            {skill.growth}
                          </span>
                          <span className="bg-gradient-to-r from-blue-500 to-teal-500 text-white px-4 py-2 rounded-full text-sm shadow-lg shadow-blue-500/20">
                            {skill.jobs} jobs
                          </span>
                        </div>
                      </div>
                      <div className="flex items-center gap-4">
                        <div className="flex-1">
                          <div className="w-full bg-slate-800/50 rounded-full h-4 border border-slate-600/50">
                            <div 
                              className="bg-gradient-to-r from-orange-500 to-yellow-500 h-4 rounded-full transition-all duration-1000 ease-out shadow-lg shadow-orange-500/30"
                              style={{ width: `${skill.demand}%` }}
                            ></div>
                          </div>
                        </div>
                        <span className="bg-gradient-to-r from-orange-500 to-yellow-500 text-white px-4 py-2 rounded-full font-bold text-sm shadow-lg shadow-orange-500/20">
                          {skill.demand}%
                        </span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'companies' && (
          <div className="space-y-6">
            <div className="glass-ultra rounded-3xl p-6 border border-white/20 shadow-2xl shadow-blue-500/10">
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
                <span className="text-2xl">🏆</span> Top Hiring Companies
              </h2>
              <div className="space-y-4">
                {companiesData.map((company, index) => (
                  <div key={index} className="group relative glass-premium rounded-xl p-5 hover:shadow-2xl hover:shadow-blue-500/20 transition-all duration-500 hover:-translate-y-1 cursor-pointer border border-white/10 overflow-hidden hover:border-blue-400/30">
                    {/* Animated background gradient */}
                    <div className="absolute inset-0 bg-gradient-to-br from-blue-500/0 via-teal-500/0 to-purple-500/0 group-hover:from-blue-500/10 group-hover:via-teal-500/10 group-hover:to-purple-500/10 transition-all duration-500"></div>
                    
                    <div className="relative z-10 flex items-center justify-between">
                      <div className="flex items-center gap-4 flex-1">
                        <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-purple-500 rounded-xl flex items-center justify-center text-white font-bold shadow-lg shadow-blue-500/20 group-hover:scale-110 transition-transform duration-500">
                          {index + 1}
                        </div>
                        <div className="flex-1">
                          <h3 className="text-white font-bold text-lg group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-blue-400 group-hover:to-teal-400 group-hover:bg-clip-text transition-all duration-500 mb-2">
                            {company.name}
                          </h3>
                          <div className="flex items-center gap-3">
                            <span className="bg-gradient-to-r from-yellow-500 to-orange-500 text-white px-3 py-1 rounded-full text-sm font-bold shadow-lg shadow-yellow-500/20">
                              ⭐ {company.rating}
                            </span>
                            <span className="text-slate-400 text-sm">•</span>
                            <span className="bg-gradient-to-r from-blue-500 to-teal-500 text-white px-3 py-1 rounded-full text-sm shadow-lg shadow-blue-500/20">
                              {company.openings} openings
                            </span>
                          </div>
                        </div>
                      </div>
                      <div className="bg-gradient-to-r from-green-500 to-emerald-500 text-white px-4 py-2 rounded-full font-bold text-sm shadow-lg shadow-green-500/20 group-hover:scale-105 transition-transform">
                        {company.growth}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'salary' && (
          <div className="space-y-6">
            <div className="glass-ultra rounded-3xl p-6 border border-white/20 shadow-2xl shadow-blue-500/10">
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
                <span className="text-2xl">💰</span> Salary Trends by Role
              </h2>
              <div className="space-y-4">
                {salaryData.map((item, index) => (
                  <div key={index} className="group relative glass-premium rounded-xl p-5 hover:shadow-2xl hover:shadow-blue-500/20 transition-all duration-500 hover:-translate-y-1 cursor-pointer border border-white/10 overflow-hidden hover:border-blue-400/30">
                    {/* Animated background gradient */}
                    <div className="absolute inset-0 bg-gradient-to-br from-blue-500/0 via-teal-500/0 to-purple-500/0 group-hover:from-blue-500/10 group-hover:via-teal-500/10 group-hover:to-purple-500/10 transition-all duration-500"></div>
                    
                    <div className="relative z-10 flex items-center justify-between">
                      <div className="flex-1">
                        <h3 className="text-white font-bold text-lg group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-blue-400 group-hover:to-teal-400 group-hover:bg-clip-text transition-all duration-500 mb-3">
                          {item.role}
                        </h3>
                        <div className="flex items-center gap-4 text-sm">
                          <span className="text-slate-300">Avg: <span className="bg-gradient-to-r from-blue-400 to-teal-400 bg-clip-text text-transparent font-semibold">{item.avg}</span></span>
                          <span className="text-slate-500">•</span>
                          <span className="text-slate-300">Growth: <span className="bg-gradient-to-r from-green-400 to-emerald-400 bg-clip-text text-transparent font-semibold">{item.growth}</span></span>
                        </div>
                      </div>
                      <div className={`group relative bg-gradient-to-r ${item.demand === 'Very High' ? 'from-red-500 to-pink-500' : item.demand === 'High' ? 'from-orange-500 to-red-500' : 'from-yellow-500 to-orange-500'} text-white px-4 py-2 rounded-full font-bold text-sm shadow-lg transition-all`}>
                        <span className="relative z-10">{item.demand}</span>
                        <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Growth Areas Section (Always Visible) */}
        <div className="glass-ultra rounded-3xl p-6 border border-white/20 shadow-2xl shadow-blue-500/10">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
            <span className="text-2xl">🚀</span> Emerging Growth Areas
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {growthAreas.map((area, index) => (
              <div
                key={index}
                className={`group relative bg-gradient-to-br ${area.color} rounded-xl p-6 text-white hover:shadow-2xl hover:shadow-blue-500/30 transition-all duration-500 hover:-translate-y-2 cursor-pointer overflow-hidden`}
              >
                {/* Animated overlay */}
                <div className="absolute inset-0 bg-gradient-to-br from-white/0 via-white/10 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
                
                <div className="relative z-10">
                  <h3 className="text-lg font-bold mb-4 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-white group-hover:to-blue-200 group-hover:bg-clip-text transition-all duration-500">
                    {area.area}
                  </h3>
                  <div className="flex items-center justify-between">
                    <div>
                      <div className="text-3xl font-extrabold mb-2 group-hover:scale-110 transition-transform">
                        {area.growth}
                      </div>
                      <div className="text-sm opacity-90">{area.jobs} opportunities</div>
                    </div>
                    <div className="text-5xl opacity-75 group-hover:scale-110 transition-transform">📈</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* SDG Impact Analysis */}
        <div className="glass-ultra rounded-3xl p-6 border border-white/20 shadow-2xl shadow-blue-500/10">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
            <span className="text-2xl">🌍</span> SDG Impact Distribution
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { sdg: 'SDG 7', name: 'Clean Energy', percentage: 35, color: 'from-yellow-500 to-orange-500' },
              { sdg: 'SDG 13', name: 'Climate Action', percentage: 28, color: 'from-green-500 to-emerald-500' },
              { sdg: 'SDG 11', name: 'Sustainable Cities', percentage: 22, color: 'from-orange-500 to-red-500' },
              { sdg: 'SDG 12', name: 'Responsible Consumption', percentage: 15, color: 'from-purple-500 to-pink-500' }
            ].map((sdg, index) => (
              <div key={index} className="group relative glass-premium rounded-xl p-6 text-center hover:shadow-2xl hover:shadow-blue-500/20 transition-all duration-500 hover:-translate-y-2 cursor-pointer border border-white/10 overflow-hidden hover:border-blue-400/30">
                {/* Animated background gradient */}
                <div className={`absolute inset-0 bg-gradient-to-br ${sdg.color.replace('from-', '').replace(' to-', '/0 via-').replace(' ', '/0 to-')} opacity-0 group-hover:opacity-10 transition-opacity duration-500`}></div>
                
                <div className="relative z-10">
                  <div className="text-4xl mb-4 group-hover:scale-110 transition-transform">🎯</div>
                  <div className="text-xl font-bold text-white mb-2 group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-blue-400 group-hover:to-teal-400 group-hover:bg-clip-text transition-all duration-500">
                    {sdg.sdg}
                  </div>
                  <div className="text-sm text-slate-300 mb-4">{sdg.name}</div>
                  <div className="text-3xl font-extrabold text-blue-400 group-hover:scale-105 transition-transform">
                    {sdg.percentage}%
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Footer Note */}
        <div className="text-center text-slate-400 text-sm pb-8 text-opacity-90">
          <p>Data updated in real-time from MariaDB • Last updated: {new Date().toLocaleString()}</p>
        </div>
      </div>
    </div>
  );
};

export default Trends;