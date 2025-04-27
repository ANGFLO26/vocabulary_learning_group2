-- Create database if not exists
CREATE DATABASE IF NOT EXISTS vocabulary_learning;
USE vocabulary_learning;

-- Create tables
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vocabulary_topics (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vocabularies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    topic_id INT NOT NULL,
    word VARCHAR(255) NOT NULL,
    meaning TEXT NOT NULL, -- Will store Vietnamese translations
    phonetic VARCHAR(100), -- Previously changed from 'example'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (topic_id) REFERENCES vocabulary_topics(id)
);

CREATE TABLE IF NOT EXISTS tests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    topic_id INT NOT NULL,
    question TEXT NOT NULL,
    correct_answer TEXT NOT NULL,   
    option1 TEXT NOT NULL,
    option2 TEXT NOT NULL,
    option3 TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (topic_id) REFERENCES vocabulary_topics(id)
);

CREATE TABLE IF NOT EXISTS test_results (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    topic_id INT NOT NULL,
    score INT NOT NULL,
    completion_time INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (topic_id) REFERENCES vocabulary_topics(id)
);

CREATE TABLE IF NOT EXISTS leaderboards (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    topic_id INT NOT NULL,
    total_score INT NOT NULL DEFAULT 0,
    tests_completed INT NOT NULL DEFAULT 0,
    average_score FLOAT NOT NULL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user_topic (user_id, topic_id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (topic_id) REFERENCES vocabulary_topics(id)
);

-- Add indexes for better query performance
ALTER TABLE vocabularies ADD INDEX idx_vocab_topic (topic_id);
ALTER TABLE tests ADD INDEX idx_test_topic (topic_id);
ALTER TABLE test_results ADD INDEX idx_result_user (user_id);
ALTER TABLE test_results ADD INDEX idx_result_topic (topic_id);
ALTER TABLE leaderboards ADD INDEX idx_leaderboard_topic (topic_id);
ALTER TABLE leaderboards ADD INDEX idx_leaderboard_score (total_score DESC);

-- Drop existing trigger if exists
DROP TRIGGER IF EXISTS update_leaderboard_after_test;

-- Create trigger for updating leaderboard
DELIMITER //

CREATE TRIGGER update_leaderboard_after_test
AFTER INSERT ON test_results
FOR EACH ROW
BEGIN
    INSERT INTO leaderboards (user_id, topic_id, total_score, tests_completed, average_score)
    SELECT 
        NEW.user_id,
        NEW.topic_id,
        SUM(score),
        COUNT(*),
        AVG(score)
    FROM test_results
    WHERE user_id = NEW.user_id AND topic_id = NEW.topic_id
    ON DUPLICATE KEY UPDATE
        total_score = VALUES(total_score),
        tests_completed = VALUES(tests_completed),
        average_score = VALUES(average_score);
END //

DELIMITER ;

-- Insert sample users
INSERT INTO users (username, password, email) VALUES
('john_doe', '$2a$10$xP1XhU7KFVrqFX8JbHkKX.u7vE9iVYQXbHp3DhHYgcHAEZrCTivXi', 'john@example.com'),
('jane_smith', '$2a$10$5J5hxP1XhU7KFVrqFX8JbHkKX.u7vE9iVYQXbHp3DhHYgcHAEZrC', 'jane@example.com'),
('bob_wilson', '$2a$10$8K5hxP1XhU7KFVrqFX8JbHkKX.u7vE9iVYQXbHp3DhHYgcHAEZrC', 'bob@example.com');

-- Insert sample vocabulary topics
INSERT INTO vocabulary_topics (name, description) VALUES
('Basic English', 'Basic vocabulary for beginners'),
('Business English', 'Vocabulary for business communication'),
('Academic English', 'Vocabulary for academic purposes'),
('Travel English', 'Vocabulary for traveling'),
('Technology English', 'Vocabulary for technology and IT');

-- Insert sample vocabularies with Vietnamese meanings
INSERT INTO vocabularies (topic_id, word, meaning, phonetic) VALUES
-- Basic English
(1, 'Hello', 'Xin chào', '/həˈloʊ/'),
(1, 'Goodbye', 'Tạm biệt', '/ˌɡʊdˈbaɪ/'),
(1, 'Thank you', 'Cảm ơn', '/ˈθæŋk juː/'),
(1, 'Please', 'Làm ơn', '/pliːz/'),
(1, 'Sorry', 'Xin lỗi', '/ˈsɑːri/'),

-- Business English
(2, 'Meeting', 'Cuộc họp', '/ˈmiːtɪŋ/'),
(2, 'Deadline', 'Hạn chót', '/ˈdedlaɪn/'),
(2, 'Budget', 'Ngân sách', '/ˈbʌdʒɪt/'),
(2, 'Negotiate', 'Đàm phán', '/nɪˈɡoʊʃieɪt/'),
(2, 'Strategy', 'Chiến lược', '/ˈstrætədʒi/'),

-- Academic English
(3, 'Research', 'Nghiên cứu', '/rɪˈsɜːrtʃ/'),
(3, 'Thesis', 'Luận văn', '/ˈθiːsɪs/'),
(3, 'Analysis', 'Phân tích', '/əˈnælɪsɪs/'),
(3, 'Methodology', 'Phương pháp luận', '/ˌmeθəˈdɑːlədʒi/'),
(3, 'Citation', 'Trích dẫn', '/saɪˈteɪʃn/'),

-- Travel English
(4, 'Passport', 'Hộ chiếu', '/ˈpæspɔːrt/'),
(4, 'Reservation', 'Đặt chỗ', '/ˌrezərˈveɪʃn/'),
(4, 'Itinerary', 'Lịch trình', '/aɪˈtɪnəreri/'),
(4, 'Currency', 'Tiền tệ', '/ˈkɜːrənsi/'),
(4, 'Destination', 'Điểm đến', '/ˌdestɪˈneɪʃn/'),

-- Technology English
(5, 'Software', 'Phần mềm', '/ˈsɔːftwer/'),
(5, 'Hardware', 'Phần cứng', '/ˈhɑːrdwer/'),
(5, 'Database', 'Cơ sở dữ liệu', '/ˈdeɪtəbeɪs/'),
(5, 'Algorithm', 'Thuật toán', '/ˈælɡərɪðəm/'),
(5, 'Interface', 'Giao diện', '/ˈɪntərfeɪs/');

-- Insert sample tests
INSERT INTO tests (topic_id, question, correct_answer, option1, option2, option3) VALUES
-- Basic English Tests
(1, 'What is the meaning of "Hello"?', 'A greeting', 'A farewell', 'A question', 'A statement'),
(1, 'When do we say "Goodbye"?', 'When leaving', 'When arriving', 'When eating', 'When sleeping'),
(1, 'What does "Thank you" express?', 'Gratitude', 'Anger', 'Sadness', 'Confusion'),
(1, 'When do we use "Please"?', 'Making requests', 'Giving orders', 'Expressing anger', 'Showing surprise'),
(1, 'What does "Sorry" mean?', 'An apology', 'A greeting', 'A question', 'A statement'),

-- Business English Tests
(2, 'What is a "Meeting"?', 'A gathering for discussion', 'A type of food', 'A form of exercise', 'A musical instrument'),
(2, 'What is a "Deadline"?', 'Latest completion time', 'A type of line', 'A form of greeting', 'A measurement unit'),
(2, 'What is a "Budget"?', 'A financial plan', 'A type of food', 'A form of exercise', 'A musical instrument'),
(2, 'What does "Negotiate" mean?', 'Discuss to reach agreement', 'To eat quickly', 'To sleep deeply', 'To run fast'),
(2, 'What is a "Strategy"?', 'A plan of action', 'A type of food', 'A form of exercise', 'A musical instrument');

-- Insert sample test results
INSERT INTO test_results (user_id, topic_id, score, completion_time) VALUES
(1, 1, 90, 300),
(1, 2, 85, 320),
(2, 1, 95, 280),
(2, 2, 88, 310),
(3, 1, 92, 290);