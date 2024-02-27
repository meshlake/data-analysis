PRAGMA foreign_keys = ON;
CREATE TABLE `Addresses` (
`address_id` INTEGER PRIMARY KEY,
`line_1` VARCHAR(255),
`line_2` VARCHAR(255),
`line_3` VARCHAR(255),
`city` VARCHAR(255),
`zip_postcode` VARCHAR(20),
`state_province_county` VARCHAR(255),
`country` VARCHAR(255),
`other_address_details` VARCHAR(255)
);
CREATE TABLE `Courses` (
`course_id` INTEGER PRIMARY KEY,
`course_name` VARCHAR(255),
`course_description` VARCHAR(255),
`other_details` VARCHAR(255)
);
CREATE TABLE `Departments` (
`department_id` INTEGER PRIMARY KEY,
`department_name` VARCHAR(255),
`department_description` VARCHAR(255),
`other_details` VARCHAR(255)
);

CREATE TABLE `Degree_Programs` (
`degree_program_id` INTEGER PRIMARY KEY,
`department_id` INTEGER NOT NULL,
`degree_summary_name` VARCHAR(255),
`degree_summary_description` VARCHAR(255),
`other_details` VARCHAR(255),
FOREIGN KEY (`department_id` ) REFERENCES `Departments`(`department_id` )
);






