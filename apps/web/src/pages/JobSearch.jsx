import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../context/LanguageContext'; // ADD THIS IMPORT

const JobSearch = () => {
  const [skills, setSkills] = useState(['Python']);
  const [location, setLocation] = useState('');
  const [salaryRange, setSalaryRange] = useState('');
  const [sdgGoal, setSdgGoal] = useState('');
  const [experienceLevel, setExperienceLevel] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [jobs, setJobs] = useState([]);
  const [searchPerformed, setSearchPerformed] = useState(false);
  const [autoDetecting, setAutoDetecting] = useState(false);
  const { user } = useAuth();
  const { t, language } = useLanguage(); // ADD THIS

  // Load featured jobs on mount
  useEffect(() => {
    setJobs(getFeaturedJobs());
  }, []);

  const getFeaturedJobs = () => [
    {
      id: 1,
      title: "Senior Solar Energy Engineer",
      company: "Tata Power Renewables",
      location: "Bengaluru, Karnataka",
      salary: "₹12-18 LPA",
      match: "95%",
      type: "Full-time",
      sdg: "SDG 7: Affordable & Clean Energy",
      sdgScore: "9/10",
      skills: ["Solar PV", "Grid Integration", "Python"],
      postedDays: 2
    },
    {
      id: 2,
      title: "Sustainability Data Analyst", 
      company: "Adani Green Energy",
      location: "Mumbai, Maharashtra",
      salary: "₹10-15 LPA",
      match: "88%",
      type: "Full-time",
      sdg: "SDG 13: Climate Action",
      sdgScore: "8/10",
      skills: ["Python", "SQL", "Power BI"],
      postedDays: 5
    },
    {
      id: 3,
      title: "Green Building Architect",
      company: "ReNew Power", 
      location: "Delhi NCR",
      salary: "₹14-20 LPA",
      match: "82%",
      type: "Full-time",
      sdg: "SDG 11: Sustainable Cities",
      sdgScore: "9/10",
      skills: ["LEED", "AutoCAD", "BIM"],
      postedDays: 1
    },
    {
      id: 4,
      title: "ESG Reporting Manager",
      company: "Suzlon Energy",
      location: "Pune, Maharashtra",
      salary: "₹15-22 LPA",
      match: "90%",
      type: "Full-time",
      sdg: "SDG 12: Responsible Consumption",
      sdgScore: "8/10",
      skills: ["ESG", "Sustainability", "Reporting"],
      postedDays: 3
    },
    {
      id: 5,
      title: "Wind Energy Analyst",
      company: "Inox Wind",
      location: "Ahmedabad, Gujarat",
      salary: "₹11-16 LPA",
      match: "85%",
      type: "Full-time",
      sdg: "SDG 7: Affordable & Clean Energy",
      sdgScore: "9/10",
      skills: ["Wind Power", "Data Analysis", "Python"],
      postedDays: 4
    },
    {
      id: 6,
      title: "Carbon Accounting Specialist",
      company: "Mahindra Sustainability",
      location: "Chennai, Tamil Nadu",
      salary: "₹12-17 LPA",
      match: "87%",
      type: "Full-time",
      sdg: "SDG 13: Climate Action",
      sdgScore: "9/10",
      skills: ["Carbon Accounting", "GHG Protocol", "Excel"],
      postedDays: 6
    }
  ];

  const handleSearch = async () => {
    if (!user) return;
    
    setIsLoading(true);
    setSearchPerformed(true);
    
    try {
      const token = localStorage.getItem('token');
      
      if (!token) {
        throw new Error('No authentication token found. Please login again.');
      }

      console.log('🔑 Using token:', token.substring(0, 20) + '...');
      console.log('🌐 Language:', language); // Debug language

      // USE THE NEW API ENDPOINT WITH LANGUAGE SUPPORT
      const response = await fetch('http://127.0.0.1:8000/api/jobs/search', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          skill_text: skills.filter(skill => skill.trim() !== ''),
          lang: language, // USE CURRENT LANGUAGE
          location: location || undefined
        })
      });
  
      console.log('📡 API Response status:', response.status);
  
      if (response.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        return;
      }
  
      if (!response.ok) {
        throw new Error(`API request failed with status: ${response.status}`);
      }
  
      const data = await response.json();
      
      // Transform backend response to match frontend format
      const transformedJobs = data.matches.map(job => ({
        id: job.id,
        title: job.job_title, // This will be translated if language != 'en'
        company: job.company, // This will be translated if language != 'en'
        location: job.location,
        salary: job.salary_range,
        match: `${Math.round(job.similarity * 100)}%`,
        type: "Full-time",
        sdg: job.sdg_impact,
        sdgScore: extractSDGScore(job.sdg_impact),
        skills: extractSkills(job.description),
        postedDays: 1,
        description: job.description // Keep description for skills extraction
      }));
  
      setJobs(transformedJobs);
    } catch (error) {
      console.error('Search failed:', error);
      // Fallback to mock data with filtering
      const filtered = getFeaturedJobs().filter(job => {
        const matchesLocation = !location || job.location.toLowerCase().includes(location.toLowerCase());
        const matchesSalary = !salaryRange || checkSalaryMatch(job.salary, salaryRange);
        const matchesExperience = !experienceLevel || true;
        return matchesLocation && matchesSalary && matchesExperience;
      });
      setJobs(filtered);
    } finally {
      setIsLoading(false);
    }
  };

  // Helper function to extract SDG score
  const extractSDGScore = (sdgImpact) => {
    const match = sdgImpact.match(/\d+\/\d+/);
    return match ? match[0] : "8/10";
  };

  // Helper function to extract skills from description
  const extractSkills = (description) => {
    const commonSkills = ['Python', 'Power BI', 'Analytics', 'Data', 'ESG', 'Solar', 'Renewable', 'Sustainability'];
    return commonSkills.filter(skill => 
      description.toLowerCase().includes(skill.toLowerCase())
    ).slice(0, 3);
  };

  const checkSalaryMatch = (jobSalary, range) => {
    const salary = parseInt(jobSalary.match(/\d+/)[0]);
    if (range === '0-10') return salary <= 10;
    if (range === '10-15') return salary >= 10 && salary <= 15;
    if (range === '15-20') return salary >= 15 && salary <= 20;
    if (range === '20+') return salary >= 20;
    return true;
  };

  const handleAutoDetectLocation = () => {
    setAutoDetecting(true);
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        () => {
          setTimeout(() => {
            setLocation('Bengaluru, Karnataka');
            setAutoDetecting(false);
          }, 1000);
        },
        () => {
          setLocation('Bengaluru, Karnataka');
          setAutoDetecting(false);
        }
      );
    }
  };

  const addSkill = () => {
    setSkills([...skills, '']);
  };

  const updateSkill = (index, value) => {
    const newSkills = [...skills];
    newSkills[index] = value;
    setSkills(newSkills);
  };

  const removeSkill = (index) => {
    if (skills.length > 1) {
      setSkills(skills.filter((_, i) => i !== index));
    }
  };

  const clearFilters = () => {
    setSkills(['Python']);
    setLocation('');
    setSalaryRange('');
    setSdgGoal('');
    setExperienceLevel('');
    setJobs(getFeaturedJobs());
    setSearchPerformed(false);
  };

  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 relative overflow-hidden">
        {/* Enhanced Background Animation */}
        <div className="absolute inset-0">
          <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-br from-blue-500/5 via-transparent to-purple-500/5 animate-pulse"></div>
          <div className="absolute top-20 right-20 w-96 h-96 bg-gradient-to-br from-cyan-400/10 to-teal-400/10 rounded-full blur-3xl animate-float"></div>
          <div className="absolute bottom-20 left-20 w-96 h-96 bg-gradient-to-br from-emerald-400/10 to-green-400/10 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }}></div>
        </div>

        <div className="max-w-2xl mx-auto text-center py-12 relative z-10">
          <div className="glass-ultra rounded-3xl p-12 border border-white/20 shadow-2xl shadow-blue-500/10">
            <div className="text-6xl mb-6 animate-bounce">🔒</div>
            <h2 className="text-3xl font-bold text-white mb-4 bg-gradient-to-r from-blue-400 to-teal-400 bg-clip-text text-transparent animate-gradient">
              {t('auth.required') || 'Authentication Required'}
            </h2>
            <p className="text-slate-300 mb-8 text-lg text-opacity-90">
              {t('auth.loginToAccess') || 'Please login to access advanced job search features'}
            </p>
            <Link
              to="/login"
              className="group relative px-8 py-4 bg-gradient-to-r from-blue-600 to-teal-600 hover:from-blue-500 hover:to-teal-500 text-white rounded-xl transition-all inline-block font-semibold shadow-xl hover:shadow-2xl transform hover:scale-105 overflow-hidden border border-blue-400/30"
            >
              <span className="relative z-10 flex items-center justify-center gap-2">
                {t('nav.signIn') || 'Go to Login'} →
              </span>
              <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
            </Link>
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

      <div className="relative z-10 max-w-7xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-extrabold text-white mb-4 tracking-tight bg-gradient-to-r from-blue-400 via-teal-400 to-purple-400 bg-clip-text text-transparent animate-gradient">
            {t('job.search') || 'Find Green Jobs'}
          </h1>
          <p className="text-slate-300 text-lg text-opacity-90">
            {t('job.discoverOpportunities') || 'Discover opportunities in sustainable technology across India'} 
            {language !== 'en' && ` (${language.toUpperCase()})`}
          </p>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Search Filters Sidebar */}
          <div className="lg:col-span-1">
            <div className="glass-ultra rounded-3xl p-6 sticky top-4 border border-white/20 shadow-2xl shadow-blue-500/10">
              <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-2">
                <span className="text-2xl">🎯</span> {t('common.filters') || 'Search Filters'}
              </h2>
              
              <div className="space-y-5">
                {/* Skills */}
                <div>
                  <label className="block text-white mb-3 text-sm font-semibold tracking-wide">
                    {t('job.skills') || 'Skills'} *
                  </label>
                  <div className="space-y-2">
                    {skills.map((skill, index) => (
                      <div key={index} className="flex gap-2 items-center group">
                        <div className="relative flex-1">
                          <input
                            type="text"
                            value={skill}
                            onChange={(e) => updateSkill(index, e.target.value)}
                            className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 placeholder-slate-400 group-hover:border-slate-500"
                            placeholder={t('job.skillsPlaceholder') || "e.g. Python, Solar"}
                          />
                          <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-blue-500/0 to-teal-500/0 group-hover:from-blue-500/10 group-hover:to-teal-500/10 transition-all duration-300"></div>
                        </div>
                        {skills.length > 1 && (
                          <button
                            onClick={() => removeSkill(index)}
                            className="px-3 py-3 bg-red-500/20 hover:bg-red-500/30 border border-red-500/30 rounded-xl transition-all text-red-400 hover:text-red-300 text-sm backdrop-blur-sm group"
                          >
                            <span className="group-hover:scale-110 transition-transform">✕</span>
                          </button>
                        )}
                      </div>
                    ))}
                  </div>
                  <button
                    onClick={addSkill}
                    className="text-blue-400 hover:text-blue-300 text-sm mt-2 flex items-center gap-2 group"
                  >
                    <span className="w-6 h-6 bg-blue-500/20 border border-blue-500/30 rounded-lg flex items-center justify-center group-hover:bg-blue-500/30 transition-all">
                      +
                    </span>
                    {t('common.addSkill') || 'Add skill'}
                  </button>
                </div>

                {/* Location */}
                <div>
                  <label className="block text-white mb-3 text-sm font-semibold tracking-wide">
                    {t('job.location') || 'Location'}
                  </label>
                  <div className="relative group">
                    <input
                      type="text"
                      value={location}
                      onChange={(e) => setLocation(e.target.value)}
                      className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 placeholder-slate-400 group-hover:border-slate-500"
                      placeholder={t('job.locationPlaceholder') || "City or state"}
                    />
                    <button
                      onClick={handleAutoDetectLocation}
                      disabled={autoDetecting}
                      className="absolute right-3 top-1/2 transform -translate-y-1/2 text-blue-400 hover:text-blue-300 transition-colors group"
                      title={t('job.autoDetect') || "Auto-detect location"}
                    >
                      {autoDetecting ? (
                        <div className="w-5 h-5 border-2 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
                      ) : (
                        <span className="text-xl group-hover:scale-110 transition-transform">📍</span>
                      )}
                    </button>
                    <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-blue-500/0 to-teal-500/0 group-hover:from-blue-500/10 group-hover:to-teal-500/10 transition-all duration-300"></div>
                  </div>
                </div>

                {/* Salary Range */}
                <div>
                  <label className="block text-white mb-3 text-sm font-semibold tracking-wide">
                    {t('job.salaryRange') || 'Salary Range (LPA)'}
                  </label>
                  <div className="relative group">
                    <select
                      value={salaryRange}
                      onChange={(e) => setSalaryRange(e.target.value)}
                      className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 appearance-none group-hover:border-slate-500"
                    >
                      <option value="">{t('common.any') || 'Any'}</option>
                      <option value="0-10">₹0 - 10L</option>
                      <option value="10-15">₹10 - 15L</option>
                      <option value="15-20">₹15 - 20L</option>
                      <option value="20+">₹20L+</option>
                    </select>
                    <div className="absolute right-4 top-1/2 transform -translate-y-1/2 pointer-events-none">
                      <svg className="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                      </svg>
                    </div>
                    <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-blue-500/0 to-teal-500/0 group-hover:from-blue-500/10 group-hover:to-teal-500/10 transition-all duration-300"></div>
                  </div>
                </div>

                {/* SDG Goal */}
                <div>
                  <label className="block text-white mb-3 text-sm font-semibold tracking-wide">
                    {t('job.sdgGoal') || 'SDG Goal'}
                  </label>
                  <div className="relative group">
                    <select
                      value={sdgGoal}
                      onChange={(e) => setSdgGoal(e.target.value)}
                      className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 appearance-none group-hover:border-slate-500"
                    >
                      <option value="">{t('job.allGoals') || 'All Goals'}</option>
                      <option value="7">SDG 7: {t('job.cleanEnergy') || 'Clean Energy'}</option>
                      <option value="11">SDG 11: {t('job.sustainableCities') || 'Sustainable Cities'}</option>
                      <option value="12">SDG 12: {t('job.responsibleConsumption') || 'Responsible Consumption'}</option>
                      <option value="13">SDG 13: {t('job.climateAction') || 'Climate Action'}</option>
                    </select>
                    <div className="absolute right-4 top-1/2 transform -translate-y-1/2 pointer-events-none">
                      <svg className="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                      </svg>
                    </div>
                    <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-blue-500/0 to-teal-500/0 group-hover:from-blue-500/10 group-hover:to-teal-500/10 transition-all duration-300"></div>
                  </div>
                </div>

                {/* Experience Level */}
                <div>
                  <label className="block text-white mb-3 text-sm font-semibold tracking-wide">
                    {t('job.experienceLevel') || 'Experience Level'}
                  </label>
                  <div className="relative group">
                    <select
                      value={experienceLevel}
                      onChange={(e) => setExperienceLevel(e.target.value)}
                      className="w-full px-4 py-3 bg-slate-800/50 border border-slate-600/50 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-300 appearance-none group-hover:border-slate-500"
                    >
                      <option value="">{t('common.any') || 'Any'}</option>
                      <option value="entry">{t('job.entryLevel') || 'Entry Level (0-2 years)'}</option>
                      <option value="mid">{t('job.midLevel') || 'Mid Level (3-5 years)'}</option>
                      <option value="senior">{t('job.seniorLevel') || 'Senior (5+ years)'}</option>
                    </select>
                    <div className="absolute right-4 top-1/2 transform -translate-y-1/2 pointer-events-none">
                      <svg className="w-5 h-5 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                      </svg>
                    </div>
                    <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-blue-500/0 to-teal-500/0 group-hover:from-blue-500/10 group-hover:to-teal-500/10 transition-all duration-300"></div>
                  </div>
                </div>

                {/* Action Buttons */}
                <div className="space-y-3 pt-4">
                  <button
                    onClick={handleSearch}
                    disabled={isLoading}
                    className="w-full group relative px-6 py-4 bg-gradient-to-r from-blue-600 to-teal-600 hover:from-blue-500 hover:to-teal-500 text-white rounded-xl font-semibold transition-all disabled:opacity-50 shadow-xl hover:shadow-2xl transform hover:scale-105 overflow-hidden border border-blue-400/30"
                  >
                    <span className="relative z-10 flex items-center justify-center gap-2">
                      {isLoading ? (
                        <>
                          <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                          {t('common.searching') || 'Searching...'}
                        </>
                      ) : (
                        <>
                          <span className="text-xl group-hover:scale-110 transition-transform">🔍</span>
                          {t('common.search') || 'Search'} {t('nav.jobs') || 'Jobs'}
                        </>
                      )}
                    </span>
                    <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
                  </button>
                  
                  <button
                    onClick={clearFilters}
                    className="w-full bg-slate-800/50 hover:bg-slate-700/50 border border-slate-600/50 text-white py-3 rounded-xl font-medium transition-all text-sm backdrop-blur-sm group"
                  >
                    <span className="flex items-center justify-center gap-2 group-hover:scale-105 transition-transform">
                      <span className="text-lg">🧹</span>
                      {t('common.clearFilters') || 'Clear Filters'}
                    </span>
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Job Results */}
          <div className="lg:col-span-2">
            <div className="glass-ultra rounded-3xl p-6 border border-white/20 shadow-2xl shadow-blue-500/10">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <span className="text-2xl">💼</span>
                  {searchPerformed 
                    ? <span className="bg-gradient-to-r from-blue-400 to-teal-400 bg-clip-text text-transparent animate-gradient">{t('job.searchResults') || 'Search Results'}</span>
                    : <span className="bg-gradient-to-r from-emerald-400 to-teal-400 bg-clip-text text-transparent animate-gradient">{t('job.featuredJobs') || 'Featured Jobs'}</span>
                  }
                  <span className="text-slate-400 font-normal">({jobs.length})</span>
                </h2>
                <div className="text-sm text-slate-400 bg-white/5 px-4 py-2 rounded-full border border-white/10">
                  {t('job.sortedBy') || 'Sorted by'}: <span className="text-blue-400 font-semibold">{t('job.bestMatch') || 'Best Match'}</span>
                </div>
              </div>

              {jobs.length === 0 ? (
                <div className="text-center py-16">
                  <div className="text-8xl mb-6 animate-float">🔍</div>
                  <h3 className="text-2xl font-bold text-white mb-4 bg-gradient-to-r from-blue-400 to-teal-400 bg-clip-text text-transparent animate-gradient">
                    {t('job.noJobs') || 'No jobs found'}
                  </h3>
                  <p className="text-slate-400 text-lg text-opacity-90">
                    {t('job.tryAdjustingFilters') || 'Try adjusting your filters'}
                  </p>
                  <div className="mt-8 flex justify-center gap-4">
                    <button
                      onClick={clearFilters}
                      className="px-6 py-3 bg-gradient-to-r from-blue-600 to-teal-600 hover:from-blue-500 hover:to-teal-500 text-white rounded-xl font-semibold transition-all shadow-xl hover:shadow-2xl transform hover:scale-105"
                    >
                      Clear Filters
                    </button>
                    <button
                      onClick={() => setSkills(['Python'])}
                      className="px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-xl font-semibold transition-all"
                    >
                      Reset Skills
                    </button>
                  </div>
                </div>
              ) : (
                <div className="space-y-4">
                  {jobs.map((job) => (
                    <div key={job.id} className="group relative glass-premium rounded-2xl p-6 hover:shadow-2xl hover:shadow-blue-500/20 transition-all duration-500 hover:-translate-y-2 cursor-pointer border border-white/10 overflow-hidden hover:border-blue-400/30">
                      {/* Animated background gradient */}
                      <div className="absolute inset-0 bg-gradient-to-br from-blue-500/0 via-teal-500/0 to-purple-500/0 group-hover:from-blue-500/10 group-hover:via-teal-500/10 group-hover:to-purple-500/10 transition-all duration-500"></div>
                      
                      <div className="relative z-10">
                        {/* Header */}
                        <div className="flex justify-between items-start mb-4">
                          <div className="flex-1">
                            <h3 className="text-xl font-bold text-white group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-blue-400 group-hover:to-teal-400 group-hover:bg-clip-text transition-all duration-500 mb-2">
                              {job.title}
                            </h3>
                            <div className="flex items-center gap-4 text-sm text-slate-300 flex-wrap">
                              <span className="flex items-center gap-2 bg-white/5 px-3 py-1 rounded-full border border-white/10">
                                <span className="text-lg">🏢</span> {job.company}
                              </span>
                              <span className="flex items-center gap-2 bg-white/5 px-3 py-1 rounded-full border border-white/10">
                                <span className="text-lg">📍</span> {job.location}
                              </span>
                              <span className="flex items-center gap-2 bg-white/5 px-3 py-1 rounded-full border border-white/10">
                                <span className="text-lg">⏰</span> {job.postedDays}d {t('common.ago') || 'ago'}
                              </span>
                            </div>
                          </div>
                          <div className="flex flex-col items-end gap-2">
                            <span className="bg-gradient-to-r from-green-500 to-emerald-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-lg shadow-green-500/20 group-hover:scale-105 transition-transform">
                              {job.match} {t('job.match') || 'Match'}
                            </span>
                            <span className="bg-blue-500/20 text-blue-400 px-4 py-2 rounded-full text-xs border border-blue-400/30 backdrop-blur-sm">
                              {job.type}
                            </span>
                          </div>
                        </div>

                        {/* Skills */}
                        <div className="flex flex-wrap gap-2 mb-4">
                          {job.skills.map((skill, idx) => (
                            <span key={idx} className="bg-slate-800/50 text-slate-300 px-3 py-2 rounded-lg text-sm border border-slate-600/50 hover:bg-slate-700/50 transition-all group-hover:border-slate-500">
                              {skill}
                            </span>
                          ))}
                        </div>

                        {/* Footer */}
                        <div className="flex justify-between items-center pt-4 border-t border-slate-700/50">
                          <div className="flex items-center gap-4">
                            <span className="bg-gradient-to-r from-blue-500 to-teal-500 text-white px-4 py-2 rounded-lg text-lg font-bold shadow-lg shadow-blue-500/20 group-hover:scale-105 transition-transform">
                              💰 {job.salary}
                            </span>
                            <span className="bg-gradient-to-r from-purple-500 to-pink-500/20 text-purple-400 px-4 py-2 rounded-lg text-sm border border-purple-400/30 backdrop-blur-sm">
                              {job.sdg} • {job.sdgScore}
                            </span>
                          </div>
                          <div className="flex gap-3">
                            <button className="group bg-slate-800/50 hover:bg-slate-700/50 border border-slate-600/50 text-white px-4 py-2 rounded-lg text-sm transition-all backdrop-blur-sm hover:scale-105">
                              <span className="flex items-center gap-2">
                                <span className="text-lg group-hover:scale-110 transition-transform">💾</span>
                                {t('common.save') || 'Save'}
                              </span>
                            </button>
                            <button className="group bg-gradient-to-r from-blue-600 to-teal-600 hover:from-blue-500 hover:to-teal-500 text-white px-6 py-2 rounded-lg text-sm transition-all font-semibold shadow-xl hover:shadow-2xl transform hover:scale-105 border border-blue-400/30">
                              <span className="flex items-center gap-2 relative z-10">
                                <span className="text-lg group-hover:scale-110 transition-transform">🚀</span>
                                {t('job.applyNow') || 'Apply Now'}
                                <span className="text-lg group-hover:translate-x-1 transition-transform">→</span>
                              </span>
                              <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
                            </button>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JobSearch;