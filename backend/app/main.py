from fastapi import FastAPI

from backend.app.schemas.subject import Subject
from backend.app.schemas.topic import Topic

app = FastAPI()

# Temporary in-memory storage. App restart hote hi ye data reset ho jayega.
subject_list = []


@app.get("/")
def home():
    return {"message": "Welcome to LearnMate AI \U0001F680"}


@app.post("/subjects")
def add_subject(subject: Subject):
    # Same subject ko different casing (Math/math) ke saath duplicate save hone se rokta hai.
    for i in subject_list:
        if subject.name.lower() == i["name"].lower():
            return {"message": "Subject already exists!"}

    # Abhi sirf subject name store kar rahe hain; future me yahin extra fields add ho sakti hain.
    subject_list.append({"name": subject.name,"topics": []})
    return {"message": "Subject added successfully", "name": subject.name}


@app.get("/subjects")
def get_subjects():
    # Current session me add kiye gaye saare subjects return karta hai.
    return subject_list

@app.post("/topics")
def add_topic(topic: Topic):
    for i in subject_list:
        if i["name"].lower() == topic.subject.lower():
            for j in i["topics"]:
                if j.lower() == topic.topic.lower():
                    return {"message": "Topic already exists!"}

            i["topics"].append(topic.topic)
            return {
                "message": "Topic added successfully",
                "data": i
            }

    return {"message": "Subject does not exist!"}




