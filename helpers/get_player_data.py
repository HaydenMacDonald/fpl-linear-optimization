import asyncio
import aiohttp
from fpl import FPL
import sys
from datetime import date
import json

async def get_player_data(include_summary=True, return_json=True):

    async with aiohttp.ClientSession() as session:
        fpl = FPL(session)
        players = await fpl.get_players(include_summary=include_summary, return_json=return_json)

    return players