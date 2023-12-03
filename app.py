import os
import sys
import time
import logging
import traceback

from aiogram.utils import executor
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from data.config import MODE

# logging settings
# log_path = "logs/bot.log"
# logging.basicConfig(filename=log_path, level=logging.INFO, filemode='a')


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        logging.info('Bot is restarting...')
        os.execv(sys.executable, [sys.executable] + sys.argv)


if __name__ == '__main__':
    if MODE == 'production':
        logging.info('Auto Reloading OFF')
        try:
            from bot_on_startup import dp, on_startup

            executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
            logging.info('Bot stopped')
        except Exception as ex:
            logging.error(f'Start Bot: ERROR: %s. TRACEBACK:\n%s' % (ex, traceback.format_exc()))
    elif MODE == 'development':
        event_handler = MyHandler()

        path = os.path.abspath(os.curdir)
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)

        observer.start()
        try:
            try:
                from bot_on_startup import dp, on_startup

                executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
                logging.info('Bot stopped')
            except Exception as ex:
                logging.error(f'Start Bot: ERROR: %s. TRACEBACK:\n%s' % (ex, traceback.format_exc()))

            while True:
                time.sleep(2)
        except Exception as ex:
            logging.error(ex)
        finally:
            observer.stop()
            observer.join()
            logging.info('Done')
