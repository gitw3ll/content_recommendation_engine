BEGIN TRANSACTION;
DROP TABLE IF EXISTS scores_data;
DROP TABLE IF EXISTS content_data;
DROP TABLE IF EXISTS user_data;
CREATE TABLE scores_data (person_id int, mental int, emotional int, diet int, wq int);
CREATE TABLE content_data (content_id int, title text);
CREATE TABLE user_data (person_id int, event_type text, content_id int);
COMMIT;
