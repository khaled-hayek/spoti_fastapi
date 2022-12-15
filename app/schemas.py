from typing import List, Optional, Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar('T')


class FollowersSchema(BaseModel):
    total: Optional[int] = None
    href: Optional[str] = None

    class Config:
        orm_mode = True


class ExternalUrlsSchema(BaseModel):
    spotify: Optional[str] = None

    class Config:
        orm_mode = True


class ImageSchema(BaseModel):
    id: int
    height: Optional[int] = None
    width: Optional[int] = None
    url: Optional[str] = None

    class Config:
        orm_mode = True


class ArtistSchema(BaseModel):
    id: str
    name: str
    popularity: Optional[int] = None
    type: Optional[str] = None
    uri: Optional[str] = None
    href: Optional[str] = None
    genres: Optional[List] = None
    images: Optional[List[ImageSchema]] = None
    followers: Optional[FollowersSchema] = None
    external_urls: Optional[ExternalUrlsSchema] = None

    class Config:
        orm_mode = True


class Response(GenericModel, Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]
