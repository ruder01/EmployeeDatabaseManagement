CREATE DATABASE Company;
USE Company;


CREATE TABLE Employees (
    employee_id INT PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    hire_date DATE,
    salary DECIMAL(10, 2),
    project_id varchar(10)
);

CREATE TABLE Projects (
    project_id INT PRIMARY KEY AUTO_INCREMENT,
    project_name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    budget DECIMAL(12, 2)
);

INSERT INTO Projects (project_name, start_date, end_date, budget)
VALUES
    ('Website Redesign', '2023-01-15', '2023-06-30', 75000),
    ('Product Launch', '2024-03-01', '2024-09-30', 150000),
    ('Market Research', '2023-08-10', '2023-12-31', 50000);
    
