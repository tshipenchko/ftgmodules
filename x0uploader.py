from .. import loader, utils  # pylint: disable=relative-beyond-top-level 
import logging 
from requests import post 
import io 
 
logger = logging.getLogger(__name__) 
 
@loader.tds 
class x0Mod(loader.Module): 
 """Uploader""" 
 strings = { 
  "name": "x0 Uploader" 
 } 
 
 async def client_ready(self, client, db): 
  self.client = client 
  
  
 @loader.sudo 
 async def xocmd(self, message): 
  await utils.answer(message, "<b>Uploading...</b>") 
  reply = await message.get_reply_message() 
  if not reply: 
   await utils.answer(message, "<b>Reply to message!</b>") 
   return 
  media = reply.media 
  if not media: 
   file = io.BytesIO(bytes(reply.raw_text, "utf-8")) 
   file.name = "txt.txt" 
  else: 
   file = io.BytesIO(await self.client.download_file(media)) 
   file.name = reply.file.name if reply.file.name else  reply.file.id+reply.file.ext 
  try: 
   x0at = post('https://x0.at', files={'file': file}) 
  except ConnectionError as e: 
   await utils.answer(message, ste(e)) 
   return 
  url = x0at.text 
  output = f'<a href="{url}">URL: </a><code>{url}</code>' 
  await utils.answer(message, output)