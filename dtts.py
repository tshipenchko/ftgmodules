# requires: pydub requests
import io
import os
import requests
from .. import loader, utils
from pydub import AudioSegment


def register(cb):
    cb(DttsMod())


class DttsMod(loader.Module):
    """Text to speech module"""

    strings = {'name': 'DTTS',
               'no_text': "I can't say nothing"}

    async def say(self, message, speaker, text, file=".dtts.mp3"):
        reply = await message.get_reply_message()
        if not text:
            if not reply:
                return await utils.answer(message, self.strings['no_text'])
            text = reply.raw_text  # use text from reply
            if not text:
                return await utils.answer(message, self.strings['no_text'])
        if message.out:
            await message.delete()  # Delete message only one is user's
        data = {"text": text}
        if speaker:
            data.update({"speaker": speaker})

        # creating file in memory
        f = io.BytesIO(requests.get("https://station.aimylogic.com/generate", data=data).content)
        f.name = file

        if check_ffmpeg():
            f, duration = to_voice(f)
        else:
            duration = None

        await message.client.send_file(message.to_id, f, voice_note=True, reply_to=reply, duration=duration)

    async def levitancmd(self, message):
        """Levitan voice"""
        await self.say(message, "levitan", utils.get_args_raw(message))

    async def oksanacmd(self, message):
        """Oksana voice"""
        await self.say(message, "oksana", utils.get_args_raw(message))

    async def yandexcmd(self, message):
        """Yandex voice"""
        await self.say(message, None, utils.get_args_raw(message))


def check_ffmpeg():
    """Checks is there ffmpeg"""
    if os.system("ffmpeg -version") == 0:
        return True
    else:
        return False


def to_voice(item):
    """Returns audio in opus format and it's duration"""
    item.seek(0)
    item = AudioSegment.from_file(item)
    m = io.BytesIO()
    m.name = "voice.ogg"
    item.split_to_mono()
    dur = len(item) / 1000
    item.export(m, format="ogg", bitrate="64k", codec="libopus")
    m.seek(0)
    return m, dur

# By @vreply @pernel_kanic @nim1love @db0mb3r and add @tshipenchko some geyporn
