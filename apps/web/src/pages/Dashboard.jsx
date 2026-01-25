import { useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const [stats, setStats] = useState({
    total_jobs: 0,
    companies: 0,
    sdg_goals: 0,
    favorites: 0,
    applications: 0,
    profile_views: 0
  });
  const [chartData, setChartData] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [timeOfDay, setTimeOfDay] = useState('');
  const { user } = useAuth();

  // Determine time-based greeting
  useEffect(() => {
    const hour = new Date().getHours();
    if (hour < 12) setTimeOfDay('Morning');
    else if (hour < 17) setTimeOfDay('Afternoon');
    else setTimeOfDay('Evening');
  }, []);

  // ✅ RECOMMENDATION FOR HACKATHON:
  // Use the polling approach - it's more reliable and achieves the same "live updates" effect without WebSocket complexity. The polling version I provided will:
  // ✅ Update stats every 15 seconds
  // ✅ Work reliably without WebSocket issues
  // ✅ Show the same real-time effect to users
  // ✅ Be easier to debug and demo

  // Real-time stats updates using polling (more reliable for demo)
  useEffect(() => {
    if (!user) return;
  
    const pollStats = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('http://127.0.0.1:8000/stats', {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        });
        
        if (response.ok) {
          const statsData = await response.json();
          setStats(prev => ({
            ...prev,
            total_jobs: statsData.total_jobs,
            companies: statsData.companies
          }));
          console.log('📊 Updated stats via polling');
        }
      } catch (error) {
        console.error('Polling error:', error);
      }
    };
  
    // Poll every 15 seconds for live updates
    const interval = setInterval(pollStats, 15000);
    
    // Initial poll
    pollStats();
  
    return () => clearInterval(interval);
  }, [user]);

  // Fetch dashboard data on initial load
  useEffect(() => {
    if (user) {
      fetchDashboardData();
    }
  }, [user]);

  const fetchDashboardData = async () => {
    setIsLoading(true);
    try {
      const token = localStorage.getItem('token');
      
      if (!token) {
        throw new Error('No authentication token found');
      }

      // Fetch stats from backend
      const statsResponse = await fetch('http://127.0.0.1:8000/stats', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStats({
          total_jobs: statsData.total_jobs || 0,
          companies: statsData.companies || 0,
          sdg_goals: statsData.sdg_goals || 0,
          favorites: statsData.favorites || 0,
          applications: statsData.applications || 0, 
          profile_views: statsData.profile_views || 0 
        });
      }

      // Fetch chart data from backend
      const chartResponse = await fetch('http://127.0.0.1:8000/dashboard', {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (chartResponse.ok) {
        const chartData = await chartResponse.json();
        // Transform backend chart data to frontend format if needed
        if (chartData.chart && chartData.chart.data) {
          setChartData(chartData.chart.data.datasets[0].data);
        }
      }

    } catch (error) {
      console.error('Dashboard data fetch failed:', error);
      // Fallback to mock data if API fails
      setStats({
        total_jobs: 547,
        companies: 52,
        sdg_goals: 15,
        favorites: 12,
        applications: 8,
        profile_views: 143
      });
    } finally {
      setIsLoading(false);
    }
  };

  // Calculate completion percentage
  const profileCompletion = useMemo(() => {
    if (!user) return 0;
    const fields = ['username', 'email', 'skills', 'location', 'bio'];
    const completed = fields.filter(field => user[field]).length;
    return Math.round((completed / fields.length) * 100);
  }, [user]);

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
              Authentication Required
            </h2>
            <p className="text-slate-300 mb-8 text-lg text-opacity-90">
              Please login to access your personalized dashboard
            </p>
            <Link
              to="/login"
              className="group relative px-8 py-4 bg-gradient-to-r from-blue-600 to-teal-600 hover:from-blue-500 hover:to-teal-500 text-white rounded-xl transition-all inline-block font-semibold shadow-xl hover:shadow-2xl transform hover:scale-105 overflow-hidden border border-blue-400/30"
            >
              <span className="relative z-10 flex items-center justify-center gap-2">
                Go to Login →
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

      <div className="relative z-10 max-w-6xl mx-auto w-full px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-extrabold text-white mb-3 tracking-tight bg-gradient-to-r from-blue-400 via-teal-400 to-purple-400 bg-clip-text text-transparent animate-gradient">
            Good {timeOfDay}, {user.username}! 👋
          </h1>
          <p className="text-slate-300 text-lg text-opacity-90">
            Your green career dashboard is ready
          </p>
        </div>

        {isLoading ? (
          <div className="flex justify-center items-center py-20">
            <div className="relative group">
              <div className="w-16 h-16 border-4 border-blue-500 border-t-transparent rounded-full animate-spin group-hover:scale-110 transition-transform"></div>
              <div className="absolute inset-0 flex items-center justify-center">
                <span className="text-2xl group-hover:scale-110 transition-transform">🌱</span>
              </div>
            </div>
          </div>
        ) : (
          <>
            {/* Profile Completion Banner */}
            {profileCompletion < 100 && (
              <div className="glass-ultra rounded-3xl p-6 bg-gradient-to-r from-orange-500/10 to-yellow-500/10 border border-orange-500/30 shadow-2xl shadow-orange-500/10 mb-8">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-lg font-bold text-white flex items-center gap-3">
                    <span className="text-2xl">⚡</span> Complete Your Profile
                  </h3>
                  <span className="bg-gradient-to-r from-orange-500 to-yellow-500 text-white px-4 py-2 rounded-full font-bold text-lg shadow-lg shadow-orange-500/20">
                    {profileCompletion}%
                  </span>
                </div>
                <div className="w-full bg-slate-800/50 rounded-full h-4 mb-3 border border-slate-600/50">
                  <div 
                    className="bg-gradient-to-r from-orange-500 to-yellow-500 h-4 rounded-full transition-all duration-1000 ease-out shadow-lg shadow-orange-500/30"
                    style={{ width: `${profileCompletion}%` }}
                  ></div>
                </div>
                <p className="text-slate-300 text-sm text-opacity-90">
                  Complete your profile to get better job matches and increase visibility to employers
                </p>
              </div>
            )}

            {/* Stats Grid */}
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4 mb-8">
              {[
                { icon: '💼', value: stats.total_jobs, label: 'Available Jobs', color: 'from-blue-500 to-blue-600', emoji: '📈' },
                { icon: '🏢', value: stats.companies, label: 'Companies', color: 'from-teal-500 to-teal-600', emoji: '🏆' },
                { icon: '🌍', value: stats.sdg_goals, label: 'SDG Goals', color: 'from-purple-500 to-purple-600', emoji: '🎯' },
                { icon: '⭐', value: stats.favorites, label: 'Saved Jobs', color: 'from-yellow-500 to-yellow-600', emoji: '💾' },
                { icon: '📨', value: stats.applications, label: 'Applications', color: 'from-green-500 to-green-600', emoji: '✅' },
                { icon: '👁️', value: stats.profile_views, label: 'Profile Views', color: 'from-pink-500 to-pink-600', emoji: '📊' }
              ].map((stat, index) => (
                <div 
                  key={index} 
                  className="group relative glass-premium rounded-2xl p-6 text-center hover:shadow-2xl hover:shadow-blue-500/20 transition-all duration-500 hover:-translate-y-2 cursor-pointer border border-white/10 overflow-hidden hover:border-blue-400/30"
                >
                  {/* Animated background gradient */}
                  <div className={`absolute inset-0 bg-gradient-to-br ${stat.color.replace('from-', '').replace(' to-', '/0 via-').replace(' ', '/0 to-')} opacity-0 group-hover:opacity-10 transition-opacity duration-500`}></div>
                  
                  <div className="relative z-10">
                    <div className="text-4xl mb-3 group-hover:scale-110 transition-transform duration-500">{stat.icon}</div>
                    <div className={`text-3xl font-extrabold bg-gradient-to-r ${stat.color} bg-clip-text text-transparent mb-2 group-hover:scale-105 transition-transform`}>
                      {stat.value}+
                    </div>
                    <div className="text-slate-300 text-sm font-medium tracking-wide">{stat.label}</div>
                  </div>
                </div>
              ))}
            </div>

            {/* Quick Actions */}
            <div className="glass-ultra rounded-3xl p-6 mb-8 border border-white/20 shadow-2xl shadow-blue-500/10">
              <h2 className="text-2xl font-bold text-white mb-6 flex items-center gap-3">
                <span className="text-2xl">⚡</span> Quick Actions
              </h2>
              <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                {[
                  { icon: '🔍', label: 'Find Jobs', path: '/job-search', color: 'from-blue-500 to-blue-600', desc: 'Search opportunities' },
                  { icon: '📈', label: 'View Trends', path: '/trends', color: 'from-teal-500 to-teal-600', desc: 'Market insights' },
                  { icon: '📝', label: 'My Resume', path: '#', color: 'from-purple-500 to-purple-600', desc: 'Update profile' },
                  { icon: '🎯', label: 'Career Path', path: '#', color: 'from-orange-500 to-orange-600', desc: 'Plan your future' }
                ].map((action, index) => (
                  <Link
                    key={index}
                    to={action.path}
                    className={`group relative bg-gradient-to-br ${action.color} text-white p-6 rounded-2xl transition-all text-center flex flex-col items-center justify-center min-h-[140px] shadow-xl hover:shadow-2xl hover:shadow-blue-500/30 transform hover:scale-105 hover:-translate-y-2 overflow-hidden`}
                  >
                    <div className="absolute inset-0 bg-gradient-to-br from-white/0 via-white/10 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
                    <div className="relative z-10">
                      <div className="text-4xl mb-3 group-hover:scale-110 transition-transform">{action.icon}</div>
                      <div className="font-bold text-base mb-2">{action.label}</div>
                      <div className="text-xs opacity-90">{action.desc}</div>
                    </div>
                  </Link>
                ))}
              </div>
            </div>

            {/* Two Column Layout */}
            <div className="grid lg:grid-cols-2 gap-6">
              {/* Recent Activity */}
              <div className="glass-ultra rounded-3xl p-6 border border-white/20 shadow-2xl shadow-blue-500/10">
                <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-3">
                  <span className="text-2xl">📊</span> Recent Activity
                </h2>
                <div className="space-y-3">
                  {[
                    { action: 'Applied to', company: 'Tata Power Renewables', time: '2 hours ago', type: 'application', color: 'bg-gradient-to-r from-green-500 to-emerald-500' },
                    { action: 'Saved job at', company: 'Adani Green Energy', time: '1 day ago', type: 'save', color: 'bg-gradient-to-r from-blue-500 to-cyan-500' },
                    { action: 'Viewed profile of', company: 'ReNew Power', time: '2 days ago', type: 'view', color: 'bg-gradient-to-r from-purple-500 to-pink-500' },
                    { action: 'Updated resume', company: 'Profile', time: '3 days ago', type: 'update', color: 'bg-gradient-to-r from-teal-500 to-blue-500' }
                  ].map((activity, index) => (
                    <div key={index} className="group relative glass-premium rounded-xl p-4 hover:shadow-2xl hover:shadow-blue-500/20 transition-all cursor-pointer border border-white/10 overflow-hidden hover:border-blue-400/30">
                      {/* Animated background gradient */}
                      <div className={`absolute inset-0 ${activity.color.replace('bg-gradient-to-r ', 'bg-gradient-to-br ')} opacity-0 group-hover:opacity-10 transition-opacity duration-500`}></div>
                      
                      <div className="relative z-10 flex items-center gap-4">
                        <div className={`w-14 h-14 rounded-xl flex items-center justify-center ${activity.color} shadow-lg group-hover:scale-110 transition-transform duration-500`}>
                          {activity.type === 'application' ? '📨' : 
                           activity.type === 'save' ? '💾' : 
                           activity.type === 'update' ? '✏️' : '👀'}
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-white font-semibold text-base truncate group-hover:text-blue-400 transition-colors">
                            {activity.action} <span className="text-blue-400 font-bold">{activity.company}</span>
                          </p>
                          <p className="text-slate-400 text-sm">{activity.time}</p>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Recommended Jobs */}
              <div className="glass-ultra rounded-3xl p-6 border border-white/20 shadow-2xl shadow-blue-500/10">
                <h2 className="text-xl font-bold text-white mb-6 flex items-center gap-3">
                  <span className="text-2xl">✨</span> Recommended For You
                </h2>
                <div className="space-y-3">
                  {[
                    { title: 'Solar Engineer', company: 'Tata Power', match: '95%', salary: '₹15-20L' },
                    { title: 'ESG Analyst', company: 'Adani Green', match: '92%', salary: '₹12-18L' },
                    { title: 'Sustainability Manager', company: 'ReNew', match: '88%', salary: '₹18-25L' }
                  ].map((job, index) => (
                    <div key={index} className="group relative glass-premium rounded-xl p-4 hover:shadow-2xl hover:shadow-blue-500/20 transition-all cursor-pointer border border-white/10 overflow-hidden hover:border-blue-400/30">
                      {/* Animated background gradient */}
                      <div className="absolute inset-0 bg-gradient-to-br from-blue-500/0 via-teal-500/0 to-purple-500/0 group-hover:from-blue-500/10 group-hover:via-teal-500/10 group-hover:to-purple-500/10 transition-all duration-500"></div>
                      
                      <div className="relative z-10">
                        <div className="flex justify-between items-start mb-3">
                          <h3 className="text-white font-bold text-lg group-hover:text-transparent group-hover:bg-gradient-to-r group-hover:from-blue-400 group-hover:to-teal-400 group-hover:bg-clip-text transition-all duration-500">
                            {job.title}
                          </h3>
                          <span className="bg-gradient-to-r from-green-500 to-emerald-500 text-white px-4 py-2 rounded-full text-sm font-bold shadow-lg shadow-green-500/20 group-hover:scale-105 transition-transform duration-500">
                            {job.match}
                          </span>
                        </div>
                        <div className="flex items-center justify-between text-sm">
                          <span className="bg-white/5 px-3 py-1 rounded-full border border-white/10 text-slate-300">
                            🏢 {job.company}
                          </span>
                          <span className="bg-gradient-to-r from-blue-500 to-teal-500 text-white px-3 py-1 rounded-full text-sm font-semibold shadow-lg shadow-blue-500/20">
                            💰 {job.salary}
                          </span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
                <Link 
                  to="/job-search"
                  className="group relative mt-4 w-full bg-gradient-to-r from-blue-600 to-teal-600 hover:from-blue-500 hover:to-teal-500 text-white py-4 rounded-xl font-semibold transition-all text-center block shadow-xl hover:shadow-2xl transform hover:scale-105 overflow-hidden border border-blue-400/30"
                >
                  <span className="relative z-10 flex items-center justify-center gap-2">
                    <span className="text-lg group-hover:scale-110 transition-transform">🚀</span>
                    View All Jobs →
                  </span>
                  <div className="absolute inset-0 bg-gradient-to-r from-white/0 via-white/20 to-white/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></div>
                </Link>
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
};

export default Dashboard;