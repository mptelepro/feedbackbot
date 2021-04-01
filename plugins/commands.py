import logging
logger = logging.getLogger(__name__)

import asyncio
from pyrogram import filters
from bot import feedback
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from translation import Translation
from config import Config

@feedback.on_message(filters.text)
async def text(c, m):
      if m.from_user.id in Config.LOGIN:
         if m.text == Config.PASS:
            Config.LOGIN.remove(m.from_user.id)
            Config.OWNER.append(m.from_user.id)
            await m.reply_text(text="From now you will receive feedbacks. Untill this bot restart.  If you want to get feedbacks permanently add your id in config vars")
         if m.text != Config.PASS:
            Config.LOGIN.remove(m.from_user.id)
            await m.reply_text(text="**Incorrect Password ⚠️**", parse_mode="markdown")
      if m.from_user.id in Config.feedback:
         button = [[
                   InlineKeyboardButton("Yes", callback_data="yes"),
                   InlineKeyboardButton("No", callback_data="cancel")
                  ]]
         markup = InlineKeyboardMarkup(button)
         await m.reply_text(text="Are you sure to send this feedback",
                            reply_markup=markup,
                            quote=True)
      try:
          if Config.SEND is not None:
             id = Config.SEND[0]
             await c.send_message(chat_id=int(id), text=m.text, parse_mode="markdown")
             Config.SEND.remove(id)
             await c.send_message(chat_id=m.chat.id, text="Notified successfully")
      except:
          pass

@feedback.on_message(filters.command(["start"]))
async def start(c, m):
      button = [[
                InlineKeyboardButton("Feedback", callback_data="feedback"),
                InlineKeyboardButton("Rules", callback_data="rules"),
                ],
                [
                InlineKeyboardButton("About", callback_data="about"),
                InlineKeyboardButton("Login", callback_data="login"),
               ]]
      markup = InlineKeyboardMarkup(button)
      await c.send_message(chat_id=m.chat.id,
                           text=Translation.START,
                           disable_web_page_preview=True,
                           reply_to_message_id=m.message_id,
                           reply_markup=markup)


@feedback.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
  chat_id = message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    user_id = message.from_user.id
    if not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator") and not user_id in Config.SUDO_USERS:
      channel = chat_db.channel
      try:
        client.get_chat_member(channel, user_id)
      except UserNotParticipant:
        try:
          sent_message = message.reply_text(
              "{}, you are **not subscribed** to my [channel](https://t.me/{}) yet. Please [join](https://t.me/{}) and **press the button below** to unmute yourself.".format(message.from_user.mention, channel, channel),
              disable_web_page_preview=True,
              reply_markup=InlineKeyboardMarkup(
                                                [[InlineKeyboardButton("UnMute Me", callback_data="onUnMuteRequest")],  
                                                [InlineKeyboardButton(text="Channel",url="https://t.me/BoX_0fFiCe"),InlineKeyboardButton(text="Project",url="https://t.me/Mai_bOTs")]])) 
        
          client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))
        except ChatAdminRequired:
          sent_message.edit("❗ **I am not an admin here.**\n__Make me admin with ban user permission and add me again.\n#Leaving this chat...__")
          client.leave_chat(chat_id)
      except ChatAdminRequired:
        client.send_message(chat_id, text=f"❗ **I am not an admin in @{channel}**\n__Make me admin in the channel and add me again.\n#Leaving this chat...__")
        client.leave_chat(chat_id)
