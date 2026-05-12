CREATE DATABASE IF NOT EXISTS covid_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE covid_db;

CREATE TABLE IF NOT EXISTS covid_data (
    id                              INT AUTO_INCREMENT PRIMARY KEY,
    iso_code                        VARCHAR(10),
    continent                       VARCHAR(50),
    location                        VARCHAR(100)   NOT NULL,
    last_updated_date               DATE,
    total_cases                     BIGINT         DEFAULT 0,
    new_cases                       BIGINT         DEFAULT 0,
    total_deaths                    BIGINT         DEFAULT 0,
    new_deaths                      BIGINT         DEFAULT 0,
    total_cases_per_million         DECIMAL(12,3)  DEFAULT 0,
    total_deaths_per_million        DECIMAL(12,3)  DEFAULT 0,
    reproduction_rate               DECIMAL(6,3)   DEFAULT 0,
    total_vaccinations              BIGINT         DEFAULT 0,
    people_vaccinated               BIGINT         DEFAULT 0,
    people_fully_vaccinated         BIGINT         DEFAULT 0,
    population                      BIGINT         DEFAULT 0,
    created_at                      TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_location  (location),
    INDEX idx_date      (last_updated_date),
    INDEX idx_continent (continent),
    UNIQUE KEY uq_location (location)
) ENGINE=InnoDB;