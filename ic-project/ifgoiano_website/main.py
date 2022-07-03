from scraping_bot import ScrapingBot


if __name__ == "__main__":
    date_string = 'Publicado: Sexta, 25 de Dezembro de 2022, 09h30 '
    sb = ScrapingBot()
    sb.fetch_all_posts()
    # print(sb.fetch_featured_post())
