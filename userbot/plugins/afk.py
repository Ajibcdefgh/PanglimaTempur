# Afk plugin from Akarata ported from uniborg
import asyncio
from datetime import datetime

from telethon import events
from telethon.tl import functions, types

from ..utils import admin_cmd
from . import BOTLOG, BOTLOG_CHATID, CMD_HELP

global USERAFK_ON
global afk_time
global last_afk_message
global afk_start
global afk_end
USERAFK_ON = {}
afk_time = None
last_afk_message = {}
afk_start = {}


@bot.on(events.NewMessage(outgoing=True))
async def set_not_afk(event):
    if event.chat_id in Config.UB_BLACK_LIST_CHAT:
        return
    global USERAFK_ON
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    back_alive = datetime.now()
    afk_end = back_alive.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = afk_end - afk_start
        time = int(total_afk_time.seconds)
        d = time // (24 * 3600)
        time %= 24 * 3600
        h = time // 3600
        time %= 3600
        m = time // 60
        time %= 60
        s = time
        endtime = ""
        if d > 0:
            endtime += f"{d}d {h}h {m}m {s}s"
        else:
            if h > 0:
                endtime += f"{h}h {m}m {s}s"
            else:
                endtime += f"{m}m {s}s" if m > 0 else f"{s}s"
    current_message = event.message.message
    if "afk" not in current_message and "on" in USERAFK_ON:
        shite = await event.client.send_message(
            event.chat_id,
            "`Aku telah kembali! Tidak lama Offline.\nOffline Sejak " + endtime + "`",
        )
        USERAFK_ON = {}
        afk_time = None
        await asyncio.sleep(5)
        await shite.delete()
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "#AFKFALSE \n`Set AFK mode to False\n"
                + "Aku telah kembali! Tidak lama Offline.\nOffline Sejak "
                + endtime
                + "`",
            )


@bot.on(
    events.NewMessage(incoming=True, func=lambda e: bool(e.mentioned or e.is_private))
)
async def on_afk(event):
    if event.fwd_from:
        return
    global USERAFK_ON
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    if afk_start != {}:
        total_afk_time = afk_end - afk_start
        time = int(total_afk_time.seconds)
        d = time // (24 * 3600)
        time %= 24 * 3600
        h = time // 3600
        time %= 3600
        m = time // 60
        time %= 60
        s = time
        endtime = ""
        if d > 0:
            endtime += f"{d}d {h}h {m}m {s}s"
        else:
            if h > 0:
                endtime += f"{h}h {m}m {s}s"
            else:
                endtime += f"{m}m {s}s" if m > 0 else f"{s}s"
    current_message_text = event.message.message.lower()
    if "afk" in current_message_text:
        # userbot's should not reply to other userbot's
        # https://core.telegram.org/bots/faq#why-doesn-39t-my-bot-see-messages-from-other-bots
        return False
    if USERAFK_ON and not (await event.get_sender()).bot:
        msg = None
        message_to_reply = (
            f"**Aku Sedang Offline**\n\n**Offline Sejak :** `{endtime}` **yang lalu** \n**Karena : **{reason}"
            if reason
            else f"**Aku Sedang Offline**\n\n**Offline Sejak :** `{endtime}`\n**Karena : **`Sedang Sibuk`"
        )
        if event.chat_id not in Config.UB_BLACK_LIST_CHAT:
            msg = await event.reply(message_to_reply)
        if event.chat_id in last_afk_message:
            await last_afk_message[event.chat_id].delete()
        last_afk_message[event.chat_id] = msg
        hmm = await event.get_chat()
        if Config.PM_LOGGR_BOT_API_ID:
            await asyncio.sleep(5)
            if not event.is_private:
                await event.client.send_message(
                    Config.PM_LOGGR_BOT_API_ID,
                    f"#AFK_TAGS \n<b>Group : </b><code>{hmm.title}</code>\
                            \n<b>Message : </b><a href = 'https://t.me/c/{hmm.id}/{event.message.id}'> link</a>",
                    parse_mode="html",
                    link_preview=False,
                )


@bot.on(admin_cmd(pattern=r"afk ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    global USERAFK_ON
    global afk_time
    global last_afk_message
    global afk_start
    global afk_end
    global reason
    USERAFK_ON = {}
    afk_time = None
    last_afk_message = {}
    afk_end = {}
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    if not USERAFK_ON:
        input_str = event.pattern_match.group(1)
        if ";" in input_str:
            msg, link = input_str.split(";", 1)
            reason = f"[{msg}]({link})"
        else:
            reason = input_str
        last_seen_status = await event.client(
            functions.account.GetPrivacyRequest(types.InputPrivacyKeyStatusTimestamp())
        )
        if isinstance(last_seen_status.rules, types.PrivacyValueAllowAll):
            afk_time = datetime.now()
        USERAFK_ON = f"on: {reason}"
        if reason:
            await edit_delete(event, f"`Aku Akan Offline Karena ~` {reason}", 5)
        else:
            await edit_delete(event, f"`Aku Akan Offline `", 5)
        if BOTLOG:
            if reason:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"#AFKTRUE \nSet AFK mode to True, and Reason is {reason}",
                )
            else:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"#AFKTRUE \nSet AFK mode to True, and Reason is Not Mentioned",
                )


CMD_HELP.update(
    {
        "afk": "__**Nama Plugin :** Afk__\
\n\n✅** CMD ➥** `.afk` [Optional Reason]\
\n**Digunakan   ➥  **Memberitahu bahwa kamu sedang offline.\nMembalas pesan mereka yang men tag akun mu \
\n\n**Catatan :** jika Kamu ingin afk dengan menggunakan hyper link [ ; ] Setelah alasan, lalu tempel tautan media.\
\n**Contoh :** `.afk sekarang sibuk ;<Media_link>`\
"
    }
)
