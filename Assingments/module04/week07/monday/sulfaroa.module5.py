from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

engine = create_engine('sqlite:///people-pets.db', echo=True)
Base = declarative_base()
metadata = MetaData(engine)
Session = sessionmaker(bind=engine)
session = Session()


class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, Sequence('person_id_seq'), primary_key=True)
    name = Column(String)
    age = Column(Integer)
    occupation = Column(String)

    pets = relationship("Pet", back_populates='owner', cascade="all, delete, delete-orphan")

    relationships = relationship('Person',
                                 secondary=relationship,
                                 primaryjoin=id == people_relationships.person_1_id,
                                 secondaryjoin=id == people_relationships.person_2_id)

    def __repr__(self):
        return "<Person(name='%s', age='%s', occupation='%s')>" % (self.name, self.age, self.occupation)


class Pet(Base):
    __tablename__ = 'pets'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    type = Column(String)
    owner_id = Column(Integer, ForeignKey('people.id'))

    owner = relationship("Person", back_populates='pets')

    friends = relationships = relationship('Pet',
                                           secondary=relationship,
                                           primaryjoin=id == pet_friends.pet_1_id,
                                           secondaryjoin=id == pet_friends.pet_2_id)

    def __repr__(self):
        return "<Pet(name='%s', age='%s', type='%s', owner_id='%s')>" % (self.name, self.age, self.type, self.owner)


class Relationship(Base):
    __tablename__ = 'people_relationships'

    id = Column(Integer, primary_key=True)
    person_1_id = Column(Integer)
    person_2_id = Column(Integer)
    type = Column(String)


class Friendship(Base):
    __tablename__ = 'pet_friends'

    id = Column(Integer, primary_key=True)
    pet_1_id = Column(Integer)
    pet_2_id = Column(Integer)
    type = Column(String)


people = Table('people', metadata,
               Column('id', Integer(), primary_key=True, nullable=False),
               Column('name', String()),
               Column('age', Integer()),
               Column('occupation', String()), schema=None)

pets = Table('pets', metadata,
             Column('id', Integer(), primary_key=True, nullable=False),
             Column('name', String()),
             Column('age', Integer()),
             Column('type', String()),
             Column('owner_id', Integer, ForeignKey('people.id')), schema=None)

people_relationships = Table('people_relationships', Base.metadata,
                             Column('id', Integer(), primary_key=True, nullable=False),
                             Column('person_1_id', Integer, ForeignKey('people.id'), primary_key=True),
                             Column('person_2_id', Integer, ForeignKey('people.id'), primary_key=True),
                             Column('type', String)
                             )

pet_friends = Table('pet_friends', Base.metadata,
                    Column('id', Integer(), primary_key=True, nullable=False),
                    Column('pet_1_id', Integer, ForeignKey('pets.id'), primary_key=True),
                    Column('pet_2_id', Integer, ForeignKey('pets.id'), primary_key=True),
                    Column('type', String)
                    )


def createPerson(name=None, age=None, occupation=None):
    new_person = Person(name=name, age=age, occupation=occupation)
    session.add(new_person)
    session.commit()

    return new_person


def findPeople(id=None, name=None, age=None, occupation=None):
    if id is None and name is None and age is None and occupation is None:
        searched = session.query(Person).all()
        return searched
    if id is not None:
        person = session.query(Person).get(id)
        return person

    query = 'SELECT * FROM people where '

    query_dict = {}

    if name is not None:
        query_dict['name'] = name
    if age is not None:
        query_dict['age'] = str(age)
    if occupation is not None:
        query_dict['occupation'] = occupation

    for key, value in query_dict.items():
        if key == 'age':
            query += key
            query += '='
            query += value + ' '
            query += ' and '
        else:
            query += key
            query += ' like '
            query += '"%' + value + '%"' + ' '
            query += ' and '

    query = query[:-5]
    query = text(query)
    return session.execute(query).fetchall()


def deletePerson(person):
    """
    deletes person and all pets associated with them
    :param person: person to delete
    :return: count to objects deleted
    """
    count = len(person.pets)
    session.delete(person)

    return count


def createPet(person=None, name=None, age=None, type=None):
    # cant add pet if parent DNE
    if person is not None:
        new_pet = Pet(name=name, age=age, type=type, owner=person)
        session.add(new_pet)
        session.commit()

        return new_pet
    return


def findPets(id=None, name=None, age=None, type=None, owner_id=None):
    if id is None and name is None and age is None and type is None and owner_id is None:
        searched = session.query(Pet)
        return searched.all()

    if id is not None:
        pet = session.query(Pet).get(id)
        return pet

    if owner_id is not None:
        searched = session.query(Pet)

    query = 'SELECT * FROM pets where '

    query_dict = {}

    if name is not None:
        query_dict['name'] = name
    if age is not None:
        query_dict['age'] = str(age)
    if type is not None:
        query_dict['type'] = type

    for key, value in query_dict.items():
        if key == 'age':
            query += key
            query += '='
            query += value + ' '
            query += ' and '
        else:
            query += key
            query += ' like '
            query += '"%' + value + '%"' + ' '
            query += ' and '

    query = query[:-5]
    print(query)
    query = text(query)
    return session.execute(query).fetchall()


def deletePet(pet):
    """
    deletes pet associated with person
    :param pet: pet to delete from person's pet collection
    :return: count of objects deleted
    """
    if pet is not None:
        session.query(Pet).filter(Pet.id == pet.id).delete()
        return 1
    return 0


def show_friends(person):
    pass


def befriend(self, friend):
    if friend not in self.friends:
        self.friends.append(friend)
        friend.friends.append(self)


def unfriend(self, friend):
    if friend in self.friends:
        self.friends.remove(friend)
        friend.friends.remove(self)


def main():
    # people.create()
    # pets.create()

    # createPerson(name='toby mcschmozeby', age=20, occupation='student')
    # jim_bob = findPeople(2)
    # pet = jim_bob.pets[0]
    # print(pet)
    # deletePet(pet)

    people = findPeople(name='toby')
    pets = findPets()
    print(people)
    print(pets)

    # createPet(jim_bob, 'sugar', 2, 'cat')
    # session.delete(jim_bob)

    session.commit()


if __name__ == '__main__':
    main()
