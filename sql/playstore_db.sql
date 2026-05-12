CREATE DATABASE IF NOT EXISTS playstore_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE playstore_db;

CREATE TABLE IF NOT EXISTS app_reviews (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    app_id            VARCHAR(200)   NOT NULL,
    title             VARCHAR(300),
    reviews           BIGINT         DEFAULT 0,
    ratings           BIGINT         DEFAULT 0,
    min_installs      BIGINT         DEFAULT 0,
    score             DECIMAL(6, 4)  DEFAULT 0.0,
    offers_iap        TINYINT(1)     DEFAULT 0,
    ad_supported      TINYINT(1)     DEFAULT 0,
    released          DATE,
    ratings_per_day   INT            DEFAULT 0,
    genre             VARCHAR(100),
    genre_id          VARCHAR(100),
    price             DECIMAL(8, 2)  DEFAULT 0.00,
    rating_one_star   INT            DEFAULT 0,
    rating_two_star   INT            DEFAULT 0,
    rating_three_star INT            DEFAULT 0,
    rating_four_star  INT            DEFAULT 0,
    rating_five_star  INT            DEFAULT 0,
    created_at        TIMESTAMP      DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_genre   (genre),
    INDEX idx_score   (score),
    INDEX idx_title   (title(100)),
    UNIQUE KEY uq_app_id (app_id)
) ENGINE=InnoDB;