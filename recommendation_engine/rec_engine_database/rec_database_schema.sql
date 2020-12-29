BEGIN TRANSACTION;
CREATE TABLE content_data (content_id int, title text);
CREATE TABLE user_data (person_id int, content_id int, title text);
COMMIT;
