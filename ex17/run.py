from ex17.bot import Bot

if __name__ == '__main__':
    with Bot() as bot:
        bot.access_video_repeatedly('https://youtu.be/MDRWHW7nymc')
