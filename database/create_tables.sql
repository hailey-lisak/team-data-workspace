-- GUNNA HAVE TO CHANGE THE NAME AND STATUS VARIABLE IN ALL FILES BECAUSE NAME IS A KEYWORD IN SQL

-- 1. Create Users Table
CREATE TABLE IF NOT EXISTS users ( -- Create a new table named users if the table does not exist (this prevels crashing or throwing an error)
    user_id VARCHAR(50) PRIMARY KEY, -- PRIMARY KEY: completely unique ID for this column in a table (like an SSN)
    name VARCHAR(100) NOT NULL, -- NOT NULL: strict rule; this column CANNOT be blank
    email VARCHAR(255) UNIQUE NOT NULL, -- UNIQUE: tells Postgres to double check that no two users in the entire system share the same email address
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- TIMESTAMP: data type sepcifically for tracking dates and times
                                                   -- DEAFULT CURRENT_TIEMSTAMP: automation feature so that I don't have to manually tell Python to calculate the time a user was created
                                                            -- the second a new row hits the table, the internal clock is checked 
);

-- 2. Create Workspaces Table
CREATE TABLE IF NOT EXISTS workspaces (
    workspace_id VARCHAR(50) PRIMARY KEY,
    user_id VARCHAR(50) REFERENCES users(user_id) ON DELETE CASCADE, -- REFERENCES users(user_id): foreign key; hard link between a workspace and the user who owns it
                                                                     -- ON DELETE CASCADE: automatic cleanup rule; if a user deletes their account from the users table, Postgres will automatically find and delete their workspaces too
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Create Jobs Table (NEW!)
CREATE TABLE IF NOT EXISTS jobs (
    job_id VARCHAR(50) PRIMARY KEY,
    workspace_id VARCHAR(50) REFERENCES workspaces(workspace_id) ON DELETE CASCADE,
    status VARCHAR(50) DEFAULT 'pending', -- tracks where the pipeline is currently at; holds text like pending (default if no status is specified), processing, completed, or failed
    total_records INT DEFAULT 0, -- stores a whole numnber representing the total size of the import batch
    processed_records INT DEFAULT 0, 
    failed_records INT DEFAULT 0,        
    error_message TEXT DEFAULT NULL, -- TEXT: has no length cap unlike VARCHAR
                                     -- DEAFULT NULL: when a job starts successfully, this column is blank because there are no errors yet
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP DEFAULT NULL,    -- 
    completed_at TIMESTAMP DEFAULT NULL   -- 
);

-- 4. Create Records Table (Updated to link to jobs!)
CREATE TABLE IF NOT EXISTS records (
    record_id VARCHAR(50) PRIMARY KEY,
    workspace_id VARCHAR(50) REFERENCES workspaces(workspace_id) ON DELETE CASCADE,
    name VARCHAR(100),
    email VARCHAR(255) NOT NULL,
    company VARCHAR(100),
    city VARCHAR(100),
    notes TEXT,
    is_valid BOOLEAN DEFAULT FALSE,
    tag VARCHAR(50),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);