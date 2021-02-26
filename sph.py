# Coded by D4n1l3k300 
# add geyporno -> @tshipenchko
# t.me/tshipenchko
# t.me/D4n13l3k00 
# requires: pornhub-api 
from .. import loader, utils 
from random import choice 
from pornhub_api import PornhubApi 
@loader.tds 
class PhSrchMod(loader.Module): 
  strings = {"name": "PornHub"} 
  @loader.owner 
  async def sphcmd(self, m): 
    "Найти видео на pornhub" 
    args = utils.get_args_raw(m) 
    if args: 
      srch = args 
    else: 
      await utils.answer(m, "я не могу искать ничего :)") 
      return 
    api = PornhubApi() 
    data = api.search.search( 
    srch, 
    ordering="mostviewed", 
    period="weekly" 
    ) 
    video = choice(data.videos) 
    await utils.answer(m, f"<b>Нашёл кое-что по запросу</b> <code>{srch}</code>: <a href=\"{video.url}\">{video.title}</a>")