from sqlalchemy import Column,Integer,String
from app.database.session import Base#Imports the Base object we created in session.py. Any class that inherits from Base becomes a database table.
from sqlalchemy.orm import relationship

class Subject(Base):#This tells SQLAlchemy:"This class is a database table."

    __tablename__ = "subjects"#SQLAlchemy will create a PostgreSQL table named: subjects

    id = Column(Integer, primary_key=True,index=True)
    name = Column(String,unique=True,nullable=False)

    topics = relationship(
        "Topic",
        back_populates="subject"
    )#Topic use nahi kiya as Topic.py load nahi kiya and sxicute karte to error ata so we used string- "Topic"
#as it tells SQLAlchemy: "Don't resolve this now. I'll tell you the class name, and you can connect it later after all models are loaded."

    #The relationship is only a Python/ORM feature. It tells SQLAlchemy:-
    "Whenever someone accesses subject.topics, look in the topics table and return all rows where topics.subject_id == subject.id."

