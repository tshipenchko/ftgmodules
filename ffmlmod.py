from .. import loader, utils 
from telethon import events 
from telethon.errors.rpcerrorlist import YouBlockedUserError 
 
 
def register(cb): 
    cb(FuckingFowrarderMod()) 
     
class FuckingFowrarderMod(loader.Module): 
    """Делает копию сообщения и отправляет через @ffmlbot""" 
    strings = {'name': 'Forwarder'} 
 
    async def fcmd(self, message): 
        """Используй: .f <реплай>.""" 
        chat = "@ffmlbot" 
        reply = await message.get_reply_message() 
        if not reply: 
            await message.edit("<b>Нет реплая.</b>") 
            return 
        await message.edit("<b>Минуточку...</b>") 
        async with message.client.conversation(chat) as conv: 
            if False: pass # мне просто лень убрать, я блять с телефона прямо в телеге пишу модуль
            else: 
                try: 
                    f = await conv.send_message(reply);  await f.reply ("/f") 
                    response = conv.wait_event(events.NewMessage(incoming=True, from_users=1661783436)) 
                    response = await response 
                except YouBlockedUserError: 
                    await message.edit("<b>Разблокируй @ffmlbot</b>") 
                    return 
        await response.forward_to(message.to_id); await message.delete()