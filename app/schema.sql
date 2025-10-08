DROP TABLE IF EXISTS all_questions;
DROP TABLE IF EXISTS question_types;



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

CREATE TABLE question_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    FOREIGN KEY (question_id) REFERENCES questions(id)
);
