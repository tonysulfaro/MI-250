from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

engine = create_engine('sqlite:///music-data.db', echo=True)
Base = declarative_base()
metadata = MetaData(engine)
metadata.bind = engine
metadata.create_all()
Session = sessionmaker(bind=engine)
session = Session()

user = Table('users', metadata,
             Column('id', Integer(), primary_key=True, nullable=False),
             Column('user_name', String()),
             Column('password', String()))

playlist = Table('playlists', metadata,
                 Column('id', Integer(), primary_key=True, nullable=False),
                 Column('playlist_title', String()),
                 Column('password', String()))

album = Table('albums', metadata,
              Column('id', Integer(), primary_key=True, nullable=False),
              Column('album_title', String()),
              Column('artist_name', String()),
              Column('label', String()),
              Column('release_date', DateTime()),
              Column('other_id', String()))

song = Table('songs', metadata,
             Column('id', Integer(), primary_key=True, nullable=False),
             Column('song_name', String()),
             Column('album_id', Integer, ForeignKey('albums.id')), schema=None)

album_association_user = Table('album_association_user', metadata,
                               Column('user_id', Integer, ForeignKey('users.id')),
                               Column('album_id', Integer, ForeignKey('albums.id'))
                               )

playlist_association_user = Table('playlist_association_user', metadata,
                                  Column('user_id', Integer, ForeignKey('users.id')),
                                  Column('playlist_id', Integer, ForeignKey('playlists.id'))
                                  )

song_association_playlist = Table('song_association_playlist', metadata,
                                  Column('playlist_id', Integer, ForeignKey('playlists.id')),
                                  Column('song_id', Integer, ForeignKey('songs.id'))
                                  )


class Album(Base):
    __tablename__ = 'albums'
    id = Column(Integer, primary_key=True)
    album_title = Column(String)
    artist_name = Column(String)
    label = Column(String)
    release_date = Column(DateTime)
    other_id = Column(String)
    songs = relationship("Song", back_populates='album', cascade="all, delete, delete-orphan")


class Song(Base):
    __tablename__ = 'songs'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    album = relationship("Album", back_populates='songs')


class Playlist(Base):
    __tablename__ = 'playlists'
    id = Column(Integer, primary_key=True)
    playlist_title = Column(String)
    artist_name = Column(String)
    songs = relationship("Songs", secondary=song_association_playlist)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    user_name = Column(String)
    password = Column(String)
    albums = relationship("Album", secondary=album_association_user)
    playlists = relationship("Playlist", secondary=playlist_association_user)


def main():
    # user.create()
    # album.create()
    # playlist.create()
    # song.create()
    # album_association_user.create()
    # playlist_association_user.create()
    # song_association_playlist.create()

    jim_bob = session.query(User).get(1)
    print(jim_bob)

    session.commit()


if __name__ == '__main__':
    main()
