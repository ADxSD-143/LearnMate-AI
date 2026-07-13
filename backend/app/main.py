from fastapi import FastAPI

app = FastAPI()
subject_list=[]#temporary in memory storage

@app.get("/")
def home():
    return {"message": "Welcome to LearnMate AI 🚀"}

from backend.app.schemas.subject import Subject
@app.post("/subjects")
def add_subject(subject: Subject):
    for i in subject_list:
        if subject.name.lower() == i["name"].lower():
            return {"message": "Subject already exists!"}

    subject_list.append({ "name": subject.name})
    return {"message": "Subject added successfully",
            "name": subject.name}
@app.get("/subjects")
def get_subjects():
    return subject_list

