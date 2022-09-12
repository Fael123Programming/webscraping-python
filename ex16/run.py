from ex16.bot import Bot

if __name__ == '__main__':
    with Bot() as bot:
        bot.click_button_on_mais_brasil_platform_main_menu('Convênios')
        bot.click_submenu_option('Consultar Convênios/Pré-Convênios')
        bot.consult_convenio("911569")
        bot.click_convenio_tab_and_subtab('TCE', 'TCE')
