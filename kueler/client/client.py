import discord
import asyncio
import logging

import kueler.client.getkey as _getkey
import kueler.handlers

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='data/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

class KuelerClient(discord.Client):
    async def on_ready(self):
        await self.change_presence(game=discord.Game(name='You Count', url='https://github.com/UnsignedByte/Counter-Bot', type=1))
    async def on_message(self, message):
        await kueler.handlers.on_message(self, message)
    async def on_message_edit(self, before, after):
        await kueler.handlers.on_message(self, after)
Kueler = KuelerClient()

def runBot():
    Kueler.run(_getkey.key())

if __name__ == "__main__":
    print("Auth key is %s" % _getkey.key())
