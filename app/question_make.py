from bs4 import BeautifulSoup
import csv
from app.config import paths
import re

class question:

    def __init__(self, title, answers, correct_answer, category, id, types, image=None):
        self.title = title
        self.answers = answers
        self.correct_answer = correct_answer
        self.category = category
        self.id = id
        self.image = image
        self.types = types





class questionmaker:
     def __init__(self, tablepath):
        self.tablepath = tablepath
        self.questionlist = []

     def splitTitle(self, title):
            try:
                id = int (title [0:4])
            except:
                 raise ValueError("no id found")
            new_title = title [5:]


            dict = {"id": id, "title": new_title.strip()}
            return  dict
            


     def makeQuestion(self, row):


        missing_fields = []
        if not row.get('title2'):
            missing_fields.append('title2')
        if not row.get('description4'):
            missing_fields.append('description4')



        if missing_fields:
            raise ValueError(f"Missing fields: {', '.join(missing_fields)}")

        title_dict = self.splitTitle (row["title2"])

        title = title_dict["title"]
        id = title_dict["id"]
        readtext = self.readHTML(row["description4"])
        answers = readtext["answers"]
        correct_answer = readtext["correct_answer"] 
        category = row["category"]
        types = readtext ["types"]
        if "image" in readtext: 
            image = readtext["image"]
            return question(title, answers, correct_answer, category, id, types, image)

        return question(title, answers, correct_answer, category, id, types)

     def makeList(self):
        questions = []
        with open(self.tablepath, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate (reader, start=2):
                try:
                    question = self.makeQuestion(row)
                    questions.append(question)
                except ValueError as e:
                    print(f"Error processing row {i}: {e}")
                    continue
        return questions


     def readHTML(self, text):
        def normalize_letters(s):
            replacements = {
                '\u0410': 'A', '\u0412': 'B', '\u0415': 'E', '\u041a': 'K',
                '\u041c': 'M', '\u041d': 'H', '\u041e': 'O', '\u0420': 'P',
                '\u0421': 'C', '\u0422': 'T', '\u0425': 'X'
            }
            return ''.join(replacements.get(ch, ch) for ch in s)

        soup = BeautifulSoup(text, 'html.parser')

        if not soup.find_all("li"):
            raise ValueError("answers not html formatted")

        answers = []
        correct_answer = None
        for i, li in enumerate(soup.find_all("li")):
            answers.append(li.getText(strip=True))
            if li.find("span", id=lambda x: x and x.startswith("correctAnswer")):
                correct_answer = i

        if correct_answer is None:
            raise ValueError("Missing correct answer")
        if len(answers) != 4:
            raise ValueError("There are no 4 answers")

        type_span = soup.find('span', style=lambda s: s and 'float: left' in s)
        if not type_span:
            raise ValueError("Missing question types")

        text = type_span.get_text(strip=True)
        types = re.findall(r'«(.*?)»', text)
        types = [normalize_letters(t.strip().upper()) for t in types]

        image = soup.img["src"] if soup.img else None
        return {
            "answers": answers,
            "correct_answer": correct_answer,
            "image": image,
            "types": types
        } if image else {
            "answers": answers,
            "correct_answer": correct_answer,
            "types": types
        }


