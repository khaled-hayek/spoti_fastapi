from typing import List

from sqlalchemy.orm import Session, joinedload

from schemas import ArtistSchema, ImageSchema, FollowersSchema, ExternalUrlsSchema
from model import Artist, Images, Followers, Externalurls


def get_artist(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Artist).offset(skip).limit(limit).options(joinedload("images"), joinedload("followers"),
                                                              joinedload("external_urls")).all()


def get_artist_by_id(db: Session, artist_id: str):
    return db.query(Artist).filter(Artist.id == artist_id).options(joinedload("images"), joinedload("followers"),
                                                                   joinedload("external_urls")).first()


def create_artist(db: Session, artist: ArtistSchema):
    _artist = Artist(id=artist.id, name=artist.name, popularity=artist.popularity, type=artist.type, uri=artist.uri,
                     href=artist.href, genres=artist.genres)
    db.add(_artist)
    db.commit()
    db.refresh(_artist)
    create_image(db, artist.images, artist.id)
    create_follower(db, artist.followers, artist.id)
    create_external_urls(db, artist.external_urls, artist.id)
    return _artist


def create_image(db: Session, images: List[ImageSchema], artist_id: str):
    for image in images:
        _image = Images(width=image.width, height=image.height, url=image.url, artist_id=artist_id)
        db.add(_image)
        db.commit()
        db.refresh(_image)


def create_follower(db: Session, follower: FollowersSchema, artist_id: str):
    _follower = Followers(total=follower.total, href=follower.href, artist_id=artist_id)
    db.add(_follower)
    db.commit()
    db.refresh(_follower)
    return _follower


def create_external_urls(db: Session, external_urls: Externalurls, artist_id: str):
    _external_urls = Externalurls(spotify=external_urls.spotify, artist_id=artist_id)
    db.add(_external_urls)
    db.commit()
    db.refresh(_external_urls)
    return _external_urls


def remove_artist(db: Session, artist_id: str):
    _artist = get_artist_by_id(db=db, artist_id=artist_id)
    db.delete(_artist)
    db.commit()


def update_artist(db: Session, artist_id: str, artist: ArtistSchema):
    _artist = get_artist_by_id(db=db, artist_id=artist_id)

    for key, value in artist.__dict__.items():
        if hasattr(_artist, key) and isinstance(value, (int, float, bool, str)):
            setattr(_artist, key, value)
        elif isinstance(value, FollowersSchema):
            _artist.followers.total = artist.followers.total
            _artist.followers.href = artist.followers.href
        elif isinstance(value, ExternalUrlsSchema):
            _artist.external_urls.spotify = artist.external_urls.spotify
        elif isinstance(value, list):
            if key == "genres":
                _artist.genres = artist.genres
            elif key == "images":
                for image in _artist.images:
                    for im in artist.images:
                        if image.id == im.id:
                            image.width = im.width
                            image.height = im.height
                            image.url = im.url

    db.commit()
    db.refresh(_artist)
    return _artist
