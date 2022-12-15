from fastapi import APIRouter, Depends

from schemas import Response, ArtistSchema
from config import SessionLocal
from sqlalchemy.orm import Session
import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/artists")
async def get(db: Session = Depends(get_db)):
    artists = crud.get_artist(db, 0, 100)
    return artists


@router.get("/artist/{artist_id}")
async def get_by_id(artist_id: str, db: Session = Depends(get_db)):
    artist = crud.get_artist_by_id(db, artist_id)
    return artist


@router.post('/create')
async def create(request: ArtistSchema, db: Session = Depends(get_db)):
    crud.create_artist(db=db, artist=request)
    return Response(code=200, status="ok", message="Added ...", ).dict(exclude_none=True)


@router.delete('/delete/{artist_id}')
async def delete(artist_id: str, db: Session = Depends(get_db)):
    crud.remove_artist(db=db, artist_id=artist_id)
    return Response(code=200, status="ok", message="Deleted ...", ).dict(exclude_none=True)


@router.put('/update/{artist_id}')
async def update(request: ArtistSchema, artist_id: str, db: Session = Depends(get_db)):
    print(request.images)
    _artist = crud.update_artist(db=db, artist_id=artist_id, artist=request)
    return _artist
