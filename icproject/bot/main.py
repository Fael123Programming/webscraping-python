from icproject.bot.bot import Bot
from datetime import datetime
from icproject.database.database_connection import DatabaseConnection
from icproject.bot.post import Post

if __name__ == "__main__":
    bot = Bot()
    bot.print_title_and_description_maximum_sizes()
    # bot.export_post_urls_to_csv()
    # posts = bot.get_posts_data()
    # print('-' * 150)
    # print(f'Total of {len(posts)} posts fetched')
    # print(f'Timestamp: {datetime.now()}')
    # conn = DatabaseConnection()
    # conn.connect()
    # conn.insert_post(
    #     Post(
    #         1,
    #         'Title',
    #         datetime.now(),
    #         None,
    #         'Ementa definida pelo professor. Fundamentos da linguagem Python: Objetos nativos, terminologia, regras '
    #         'de escopo, polimorfismo. Objetos em Python: Encapsulamento, herança múltipla, exemplos de APIs. Padrões '
    #         'de Projetos em Python. Mineração de dados em Python.Ementa definida pelo professor. Fundamentos da '
    #         'linguagem Python: Objetos nativos, terminologia, regras de escopo, polimorfismo. Objetos em Python: '
    #         'Encapsulamento, herança múltipla, exemplos de APIs. Padrões de Projetos em Python. Mineração de dados '
    #         'em Python.',
    #         None
    #     )
    # )
    # conn.disconnect()
