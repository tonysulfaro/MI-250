from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///test.db', echo=True)
Base = declarative_base()
metadata = MetaData(engine)


class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    occupation = Column(String)

    def __repr__(self):
        return "<User(name='%s', age='%s', occupation='%s')>" % (self.name, self.age, self.occupation)


class Pet(Base):
    __tablename__ = 'pets'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    type = Column(String)
    owner = Column(Integer)

    def __repr__(self):
        return "<User(name='%s', age='%s', type='%s', owner='%s')>" % (self.name, self.age, self.type, self.owner)


people = Table('people', metadata,
               Column('id', Integer(), primary_key=True, nullable=False),
               Column('name', String()),
               Column('age', Integer()),
               Column('occupation', String()), schema=None)


def createPerson(params):
    pass


def findPeople(params):
    pass


def deletePerson(person):
    pass


def createPet(person, params):
    pass


def findPets(params):
    pass


def deletePet(person):
    pass


def main():

    Session = sessionmaker(bind=engine)
    session = Session()

    #people.create()



    print(Person.__tablename__)
    test_person = Person(name='persony mcpersonface', age=29, occupation='underwater basket weaver')
    session.add(test_person)
    session.commit()

    our_user = session.query(Person).filter_by(age=29).first()
    print(our_user)


if __name__ == '__main__':
    main()
