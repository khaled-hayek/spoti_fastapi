from sqlalchemy import ARRAY, BigInteger, Column, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Artist(Base):
    __tablename__ = 'artist'

    id = Column(String(255), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    popularity = Column(Integer, nullable=False)
    type = Column(String(255), nullable=False)
    uri = Column(String(255), nullable=False)
    href = Column(String(255), nullable=False)
    genres = Column(ARRAY(String(length=255)), nullable=False)

    external_urls = relationship('Externalurls', uselist=False, back_populates='artist', cascade="all, delete")
    followers = relationship('Followers', uselist=False, back_populates='artist', cascade="all, delete")
    images = relationship('Images', back_populates='artist', cascade="all, delete")


class Externalurls(Base):
    __tablename__ = 'externalurls'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    spotify = Column(String(255), nullable=False)
    artist_id = Column(ForeignKey('artist.id', deferrable=True, initially='DEFERRED'), nullable=False, unique=True)

    artist = relationship('Artist', back_populates='external_urls')


class Followers(Base):
    __tablename__ = 'followers'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    total = Column(Integer, nullable=False)
    artist_id = Column(ForeignKey('artist.id', deferrable=True, initially='DEFERRED'), nullable=False, unique=True)
    href = Column(String(255))

    artist = relationship('Artist', back_populates='followers')


class Images(Base):
    __tablename__ = 'images'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    height = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    url = Column(String(255), nullable=False)
    artist_id = Column(ForeignKey('artist.id', deferrable=True, initially='DEFERRED'), nullable=False, index=True)

    artist = relationship('Artist', back_populates='images')
