DROP TABLE IF EXISTS all_quetions;
DROP TABLE IF EXISTS quetion_log;
DROP TABLE IF EXISTS users;



CREATE TABLE all_questions (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    answer_0 TEXT NOT NULL,
    answer_1 TEXT NOT NULL,
    answer_2 TEXT NOT NULL,
    answer_3 TEXT NOT NULL,
    correct_answer INTEGER NOT NULL,
    category TEXT NOT NULL,
    image TEXT
);


CREATE TABLE user (
    user_id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);


CREATE TABLE question_log (
    log_id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL, 
    date_answered TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    number_of_answers TIMESTAMP NOT NULL,
    date_next_answer TIMESTAMP NOT NULL,
    FOREIGN KEY (user_id) REFERENCES user (id),
    FOREIGN KEY (question_id) REFERENCES all_quetions (id)
);

