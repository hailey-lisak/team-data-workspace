-- 1. Create Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Create Workspaces Table
CREATE TABLE IF NOT EXISTS workspaces (
    workspace_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES users(user_id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Create Jobs Table (NEW!)
CREATE TABLE IF NOT EXISTS jobs (
    job_id VARCHAR(50) PRIMARY KEY,
    workspace_id VARCHAR(50) REFERENCES workspaces(workspace_id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'pending', -- pending, processing, completed, failed
    total_rows INT DEFAULT 0,
    processed_rows INT DEFAULT 0,
    failed_rows INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Create Records Table (Updated to link to jobs!)
CREATE TABLE IF NOT EXISTS records (
    record_id VARCHAR(50) PRIMARY KEY,
    workspace_id VARCHAR(50) REFERENCES workspaces(workspace_id) ON DELETE CASCADE,
    job_id VARCHAR(50) REFERENCES jobs(job_id) ON DELETE SET NULL, -- Links record to the import job
    name VARCHAR(100),
    email VARCHAR(255) NOT NULL,
    company VARCHAR(100),
    city VARCHAR(100),
    notes TEXT,
    is_valid BOOLEAN DEFAULT TRUE,
    tag VARCHAR(50),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);