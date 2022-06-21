#    Haruka Aya (A telegram bot project)
#    Copyright (C) 2017-2019 Paul Larsen
#    Copyright (C) 2019-2021 Akito Mizukito (Haruka Network Development)

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.

#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import random, io
import os

from typing import List
from telegram import Update, Bot, ParseMode, Message
from telegram.ext import run_async

from haruka import dispatcher
from haruka.modules.disable import DisableAbleCommandHandler
from telegram.utils.helpers import escape_markdown
from haruka.modules.helper_funcs.extraction import extract_user
from haruka.modules.tr_engine.strings import tld, tld_list


@run_async
def runs(bot: Bot, update: Update):
    chat = update.effective_chat
    update.effective_message.reply_text(
        random.choice(tld_list(chat.id, "jokes_runs_list")))


@run_async
def slap(bot: Bot, update: Update, args: List[str]):
    chat = update.effective_chat
    msg = update.effective_message

    # reply to correct message
    reply_text = msg.reply_to_message.reply_text if msg.reply_to_message else msg.reply_text

    # get user who sent message
    if msg.from_user.username:
        curr_user = f"@{escape_markdown(msg.from_user.username)}"
    else:
        curr_user = f"[{msg.from_user.first_name}](tg://user?id={msg.from_user.id})"

    if user_id := extract_user(update.effective_message, args):
        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        if slapped_user.username == "RealAkito":
            reply_text(tld(chat.id, "jokes_not_doing_that"))
            return
        if slapped_user.username:
            user2 = f"@{escape_markdown(slapped_user.username)}"
        else:
            user2 = f"[{slapped_user.first_name}](tg://user?id={slapped_user.id})"

    else:
        user1 = f"[{bot.first_name}](tg://user?id={bot.id})"
        user2 = curr_user

    temp = random.choice(tld_list(chat.id, "jokes_slaps_templates_list"))
    item = random.choice(tld_list(chat.id, "jokes_items_list"))
    hit = random.choice(tld_list(chat.id, "jokes_hit_list"))
    throw = random.choice(tld_list(chat.id, "jokes_throw_list"))
    itemp = random.choice(tld_list(chat.id, "jokes_items_list"))
    itemr = random.choice(tld_list(chat.id, "jokes_items_list"))

    repl = temp.format(user1=user1,
                       user2=user2,
                       item=item,
                       hits=hit,
                       throws=throw,
                       itemp=itemp,
                       itemr=itemr)

    reply_text(repl, parse_mode=ParseMode.MARKDOWN)


__help__ = True

RUNS_HANDLER = DisableAbleCommandHandler("runs", runs, admin_ok=True)
SLAP_HANDLER = DisableAbleCommandHandler("slap",
                                         slap,
                                         pass_args=True,
                                         admin_ok=True)

dispatcher.add_handler(RUNS_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)
