# ./models.py
from sqlalchemy import INTEGER, Column, ForeignKey, String, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True
    id = Column(INTEGER(), primary_key=True)


class Person(BaseModel):
    __tablename__ = "person"
    name = Column(String())
    cars = relationship("Car")

    def to_dict(self):
        return {"name": self.name, "cars": [{"brand": car.brand} for car in self.cars]}


class RequestPerformance(BaseModel):
    __tablename__ = "car"

    key = Column(String())
    start = Column(DateTime())
    pending = Column(DateTime())
    end = Column(DateTime())
    
 