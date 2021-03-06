# requires: pydub
"""
Зависимости

.terminal pip3 install pydub

!Не работает на Heroku! 
Оригинал: @dekftgmodules
"""
from pydub import AudioSegment
from .. import loader, utils
from telethon import types
import io
def register(cb):
	cb(AudioConverterMod())
class AudioConverterMod(loader.Module):
	"""Конвертирование в разные форматы"""
	strings = {'name': 'AudioConverter'}
	def __init__(self):
		self.name = self.strings['name']
		self._me = None
		self._ratelimit = []
	async def client_ready(self, client, db):
		self._db = db
		self._client = client
		self.me = await client.get_me()
	async def tovoicecmd(self, message):
		""".tovoice <reply to audio>
		    Сконвертировать аудио в войс
		"""
		reply = await message.get_reply_message()
		if not reply:
			message = await utils.answer(message, "А где реплай?")
			return
		else:
			try:
				if reply.media.document.attributes[0].voice == True:
					message = await utils.answer(message, "Это войс, а не аудиофайл!")
					return
			except:
				message = await utils.answer(message, "Это не аудиофайл!")
				return
		message = await utils.answer(message, "Скачиваем...")
		au = io.BytesIO()
		await message.client.download_media(reply.media.document, au)
		au.seek(0)
		message = await utils.answer(message, "Делаем войс...")
		audio = AudioSegment.from_file(au)
		m = io.BytesIO()
		m.name="voice.ogg" 
		audio.split_to_mono()
		message = await utils.answer(message, "Экспортируем...")
		dur = len(audio)/1000
		audio.export(m, format="ogg", bitrate="64k", codec="libopus")
		message = await utils.answer(message, "Отправляем...")
		m.seek(0)
		await message.client.send_file(message.chat_id, m, reply_to=reply.id, voice_note=True, duration=dur)
		if message.out: await message.delete()

	async def toformatcmd(self, message):
		""".toformat [format] <reply to audio>
		    Сконвертировать аудио/видео/войс в нужный формат
			Поддерживаются mp3, m4a, ogg, mpeg, wav, oga
		"""
		frmts = ['ogg', 'mpeg', 'mp3', 'wav', 'oga', 'm4a', '3gp']
		reply = await message.get_reply_message()
		if not reply:
			message = await utils.answer(message, "А где реплай?")
			return
		else:
			try:
				reply.media.document.attributes[0].duration
				if utils.get_args_raw(message):
					if utils.get_args_raw(message) not in frmts:
						message = await utils.answer(message, f"Формат {utils.get_args_raw(message)} для конвертирования не поддерживается!")
						return
					formatik = utils.get_args_raw(message)
				else:
					message = await utils.answer(message, "Укажите формат конвертирования")
					return
			except:
				message = await utils.answer(message, "Это не аудиофайл!")
				return
		message = await utils.answer(message, "Скачиваем...")
		au = io.BytesIO()
		await message.client.download_media(reply.media.document, au)
		au.seek(0)
		message = await utils.answer(message, f"Конвертируем в {formatik}...")
		audio = AudioSegment.from_file(au)
		m = io.BytesIO()
		m.name="Converted_to." + formatik
		audio.split_to_mono()
		message = await utils.answer(message, "Экспортируем...")
		audio.export(m, format=formatik)
		message = await utils.answer(message, "Отправляем...")
		m.seek(0)
		await message.client.send_file(message.chat_id, m, reply_to=reply.id, attributes=[types.DocumentAttributeAudio(duration = reply.document.attributes[0].duration, title=f"Converted to " + formatik, performer="Converter")])
		if message.out: await message.delete()
