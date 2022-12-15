import asyncio
import json
from sqlalchemy.orm import Session
import httpx
from app.crud import create_artist
from app.router import get_db
from types import SimpleNamespace

artists_ids = ["4iHNK0tOyZPYnBU7nGAgpQ", "5lpH0xAS4fVfLkACg9DAuM", "0wi4yTYlGtEnbGo4ltZTib", "1GxkXlMwML1oSg5eLPiAz3",
               "38EmEgXkgK51MT2tPY0EoC",
               "4cPHsZM98sKzmV26wlwD2W", "5KEG7G8LDYlHgFDqZyEEs2", "7K78lVZ8XzkjfRSI7570FF", "49e4v89VmlDcFCMyDv9wQ9",
               "2apYMRrg5FxN4go0pfsCvf"]

token = "BQBbEvjOKZr8cQavTtsxNrw0bnPf6SwtI9e0t6SIM42f_P9ujHdeXibLQjwbo3E04Id-jsP2nbfY8ivABC4eWA8XXEZd19m8FHvz4PH1-N7TgiPKaLMQCaNdmFYH2EwLzisGBROsY52WtvWK_ob8je5QJWysDCD_qY4_bJI2WxD176-Ry1qLGyzWx843g9BUuc0"
headers = {'Accept': 'application/json', 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + token}


async def get_artist(db, client, url):
    resp = await client.get(url)
    artist_schema = json.loads(json.dumps(resp.json()), object_hook=lambda d: SimpleNamespace(**d))
    create_artist(db, artist_schema)
    return resp.json()


async def fetch(db: Session = next(get_db())):
    async with httpx.AsyncClient(headers=headers) as client:
        tasks = []
        for artist_id in artists_ids:
            url = 'https://api.spotify.com/v1/artists/{}'.format(artist_id)
            tasks.append(asyncio.create_task(get_artist(db, client, url)))

        all_artists = await asyncio.gather(*tasks)


asyncio.run(fetch())
