BEGIN TRANSACTION;
DROP TABLE IF EXISTS content_data;
DROP TABLE IF EXISTS user_data;
CREATE TABLE content_data (content_id int, title text);
CREATE TABLE user_data (person_id int, content_id int, title text);
COMMIT;
