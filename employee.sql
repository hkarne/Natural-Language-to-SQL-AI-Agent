-- This script sets up your tables
CREATE TABLE departments (
    department_id SERIAL PRIMARY KEY,
    department_name VARCHAR(255) NOT NULL
);

CREATE TABLE employees (
    employee_id INT PRIMARY KEY,
    full_name VARCHAR(255),
    department_id INT,
    job_title VARCHAR(255),
    salary INT,
    CONSTRAINT fk_department
        FOREIGN KEY(department_id)
        REFERENCES departments(department_id)
);

-- This script inserts some starter data
INSERT INTO departments (department_id, department_name) VALUES
(1, 'Data & Analytics'), (2, 'Product'), (3, 'Marketing');

-- This script loads data from your CSV file
-- PASTE YOUR ABSOLUTE FILE PATH HERE
COPY employees(employee_id, full_name, department_id, job_title, salary)
FROM 'Users/saikarne/Desktop/my_ai_agent_project/employees.csv'
DELIMITER ','
CSV HEADER;