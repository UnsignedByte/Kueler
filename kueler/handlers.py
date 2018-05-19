# Add modules here
import discord
import os
import pickle

import asyncio
import re
from kueler.translate import translate

langmap = {
    'english': 'english',
    'ipa': 'ipa',
    'i': 'ipa',
    'eng': 'english',
    'e': 'english',
    'kueler': 'kueler',
    'k': 'kueler'
}

managed_servers = []
if os.path.isfile('data/managed_servers.txt'):
    with open("data/managed_servers.txt", 'rb') as f:
        managed_servers = pickle.load(f)

message_handlers = {}

async def on_message(Kueler, msg):
    if not msg.author.bot:
        for k in message_handlers:
            match = re.match(re.compile(k, re.I | re.MULTILINE), msg.content)
            if match:
                await message_handlers[k](Kueler, msg, match)

async def trans(Kueler, msg, match):
    f = langmap[match.group('f')]
    t = langmap[match.group('t')]
    s = match.group('s')
    em = discord.Embed(title="Translating %s to %s." % (f, t), colour = 0x3db1f4)
    em.add_field(name = "Before", value = s)
    try:
        em.add_field(name = "Result", value = translate(s, f, t))
    except KeyError:
        em.add_field(name = "Result", value = "Invalid %s!" % f)
    await Kueler.send_message(msg.channel, embed=em)


message_handlers[r'translate (?:the following|this)? from (?P<f>.*?) to (?P<t>.*?):?\s+```(?P<s>(?:.|\n)*)```$']=trans
message_handlers[r'translate (?P<s>.*) from (?P<f>.*?) to (?P<t>.*?)$']=trans
