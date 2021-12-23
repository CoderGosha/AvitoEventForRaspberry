import logging
import os

import telegram

from configuration import Configuration


class ProxyBlockService:
    block_count = 0

    def __init__(self):
        configuration = Configuration()
        self.token_bot = configuration.config['TELEGRAM']['BOT_TOKEN']
        self.chat_id = configuration.config['TELEGRAM']['CHAT_ID']
        self.bot = telegram.Bot(self.token_bot)

    def is_available(self) -> bool:
        if self.block_count > 2:
            self.do_block()

        return True

    def add_block(self):
        logging.error("PROXY IS BLOCKED")
        self.block_count += 1
        self.is_available()

    def do_block(self):
        message = "PROXY IS BLOCKED %i, BOT WAS TERMINATED" % self.block_count
        logging.error(message)
        self.bot.send_message(self.chat_id, message, parse_mode=telegram.parsemode.ParseMode.HTML)
        os._exit(1)


