from youtube_bot.youtube_bot import YoutubeBot


if __name__ == '__main__':
    with YoutubeBot() as bot:
        bot.ask_channels()
        bot.get_channels_data()
        bot.display_channels_data()
