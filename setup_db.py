import sqlite3
import json

# Create SQLite database with required tables
conn = sqlite3.connect('Backend/green_jobs.db')
cursor = conn.cursor()

# Create users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    role VARCHAR(20) DEFAULT 'job_seeker',
    phone_number VARCHAR(15),
    is_verified INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
)
''')

# Create jobs table
cursor.execute('''
CREATE TABLE IF NOT EXISTS jobs (
    job_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    company VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    job_type VARCHAR(20) DEFAULT 'Full-time',
    experience_level VARCHAR(20) DEFAULT 'Mid',
    skills TEXT,
    salary DECIMAL(10,2),
    sdg_goal VARCHAR(200) DEFAULT 'SDG 7: Affordable and Clean Energy',
    sdg_score INTEGER DEFAULT 8,
    posted_by INTEGER,
    employer_id INTEGER,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    desc_vector_json TEXT,
    skills_vector_json TEXT
)
''')

# Create careers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS careers (
    career_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    required_skills TEXT,
    growth VARCHAR(50) DEFAULT 'High',
    salary_range VARCHAR(50) DEFAULT '₹6-12 LPA',
    demand INTEGER DEFAULT 80,
    category VARCHAR(100) DEFAULT 'Green Energy',
    experience_level VARCHAR(50) DEFAULT 'Mid Level',
    desc_vector_json TEXT,
    skills_vector_json TEXT
)
''')

# Create user_profiles table
cursor.execute('''
CREATE TABLE IF NOT EXISTS user_profiles (
    profile_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER UNIQUE NOT NULL,
    headline VARCHAR(200),
    summary TEXT,
    phone_number VARCHAR(15),
    current_salary DECIMAL(10,2),
    expected_salary DECIMAL(10,2),
    notice_period INTEGER,
    resume_url VARCHAR(500),
    linkedin_url VARCHAR(200),
    github_url VARCHAR(200),
    portfolio_url VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
)
''')

# Insert sample data
# Sample users
cursor.execute('''
INSERT OR IGNORE INTO users (username, email, password, full_name, role)
VALUES (?, ?, ?, ?, ?)
''', ('testuser', 'test@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeK8Jc5f7t8JZ1Ye', 'Test User', 'job_seeker'))

# Sample jobs
jobs_data = [
    (1, 'Solar Energy Engineer', 'Design and implement solar energy systems', 'Tata Power Renewables', 'Mumbai', 'Full-time', 'Mid', 'Solar PV, Engineering, Renewable Energy', 8.5, 'SDG 7: Affordable and Clean Energy', 9, 1, 1, 'active'),
    (2, 'Environmental Analyst', 'Analyze environmental impact of projects', 'Adani Green Energy', 'Ahmedabad', 'Full-time', 'Mid', 'Environmental Science, Data Analysis', 7.2, 'SDG 13: Climate Action', 8, 1, 1, 'active'),
    (3, 'Wind Farm Technician', 'Maintain wind energy systems', 'Suzlon Energy', 'Pune', 'Full-time', 'Entry', 'Mechanical Engineering, Maintenance', 5.5, 'SDG 7: Affordable and Clean Energy', 8, 1, 1, 'active'),
]

for job in jobs_data:
    cursor.execute('''
    INSERT OR IGNORE INTO jobs (job_id, title, description, company, location, job_type, experience_level, skills, salary, sdg_goal, sdg_score, posted_by, employer_id, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', job)

# Sample careers
careers_data = [
    (1, 'Renewable Energy Specialist', 'Focus on solar, wind, and other renewable energy sources', '["Solar Energy", "Wind Power", "Project Management"]', 'Very High', '₹8-15 LPA', 95, 'Renewable Energy', 'Mid to Senior'),
    (2, 'Environmental Data Scientist', 'Use data analytics to solve environmental challenges', '["Python", "Data Analysis", "Machine Learning"]', 'High', '₹10-18 LPA', 94, 'Data Science', 'Mid to Senior'),
    (3, 'Sustainability Manager', 'Implement sustainable practices and reduce environmental impact', '["Sustainability", "ESG", "Compliance"]', 'High', '₹9-16 LPA', 92, 'Sustainability', 'Mid Level'),
]

for career in careers_data:
    cursor.execute('''
    INSERT OR IGNORE INTO careers (career_id, title, description, required_skills, growth, salary_range, demand, category, experience_level)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', career)

conn.commit()
conn.close()

print("✅ SQLite database setup complete!")
print("Created tables: users, jobs, careers, user_profiles")
print("Inserted sample data for testing")