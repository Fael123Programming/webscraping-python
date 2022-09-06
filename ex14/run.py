from bot import Bot


if __name__ == '__main__':
    with Bot() as bot:
        # bot.open_multiple_tabs()
        # bot.access_frame()
        # bot.use_javascript()
        # bot.roll_page()
        # bot.drag_and_drop()
        bot.upload_file()
