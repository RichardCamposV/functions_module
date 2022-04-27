import random
import re
import requests
from io import BytesIO
from requests_html import HTMLSession
from speak_and_listen import speak, hear_me
from selenium import webdriver
from PIL import Image

COOLMOD_URL = "https://www.coolmod.com/"


def check_status_web(url):
    driver = webdriver.Firefox()
    driver.maximize_window()
    driver.get(url)


def hear_price_and_get_price():
    while True:
        try:
            price = hear_me()
            price.replace(" euros", "").replace(",", ".").replace(" con ", ".")
            final_price = float(price)
            print(final_price)
            return final_price
        except ValueError:
            speak("No he entendido el numero")


def get_coolmod_select_category(session):
    # categories are equivalent as a rounds in function start game
    max_categories = 2
    excluded_subject = ["configura tu pc a medida"]
    list_categories = []
    select_user_categories = []

    main_site = session.get(COOLMOD_URL)
    categories = main_site.html.find(".subfamilyheadertittle")

    for subject in categories:
        for link_product in subject.absolute_links:
            if subject.text.lower() not in excluded_subject and len(list_categories) < 1:
                list_categories.append([subject.text.lower(), link_product])
            elif subject.text.lower() not in excluded_subject and len(list_categories) >= 1:
                category_exist = False
                for data in list_categories:
                    if subject.text.lower() in data:
                        category_exist = True
                if not category_exist:
                    list_categories.append([subject.text.lower(), link_product])

    speak("Selecciona {} categoria(s)".format(str(max_categories)))
    for category in list_categories:
        print(category[0])
    user_select = False

    while not user_select:
        if len(select_user_categories) < max_categories:
            speak_and_print("¿Con que categorias le gustaria jugar?:")
            user_category = hear_me()
            for data in list_categories:
                if user_category.lower() in data:
                    if len(select_user_categories) < 1:
                        select_user_categories.append(data)
                        speak_and_print("Se agrego: {}, a la lista de juego", data[0])

                    elif len(select_user_categories) >= 1:
                        category_exist = False
                        for category in select_user_categories:
                            if user_category.lower() in category:
                                category_exist = True
                                speak_and_print("Ya existe: {}, en la lista de juego", category[0])

                        if not category_exist:
                            select_user_categories.append(data)
                            speak_and_print("Se agrego: {}, a la lista de juego", data[0])

        else:
            user_select = True

    return select_user_categories


def get_random_product_attributes(session, categories):
    product_page_url = random.choice(categories)

    speak_and_print("\nLa categoria con la que jugaremos sera: {}", product_page_url[0])

    product_page = session.get(product_page_url[1])
    products = product_page.html.find(".productInfo")

    product = random.choice(products)

    product_image = product.find(".productImage", first=True).html
    image = re.findall("<img src=.([A-Za-z0-9].+jpg)", product_image)
    image_src = image[0]

    product_name = product.find(".productName", first=True).text
    product_price = product.find(".discount", first=True).text

    final_price = float(product_price.replace("€", "").replace(",", "."))

    return image_src, product_name, final_price


def show_image(session, image_src):
    check_status_web(image_src)

    try:
        # img_downloaded = requests.get(image_src, verify=False)
        # Commit below line, if use above line
        img_downloaded = session.get(image_src)
        image = Image.open(BytesIO(img_downloaded.content))
        image.show()
    except requests.exceptions.ConnectionError:
        print("Connection refused")


def start_game(session, coolmod_categories, image_src, product_name, final_price):
    rounds = 2
    game_rounds = 0
    win_score = 3
    lost_score = 1
    players_list = []
    player1_score = 0
    player2_score = 0

    while game_rounds != rounds:
        print("Puntuacion\n\n"
              "Jugador 1: {}\n"
              "Jugador 2: {}\n".format(player1_score, player2_score))

        show_image(session, image_src)

        speak_and_print("El nombre del producto es: {}\n"
                        "¿Cuanto crees que vale?", product_name)

        speak_and_print("Jugador 1 es tu turno...")
        player1_price = hear_price_and_get_price()
        speak_and_print("Jugador 2 es tu turno...")
        player2_price = hear_price_and_get_price()
        players_list.append([player1_price, player2_price])

        winner_number = closest_number(players_list, final_price)

        speak_and_print("El precio era {}", final_price)

        print(players_list)

        if winner_number == player1_price:
            player1_score += win_score
            player2_score += lost_score
            speak_and_print("Jugador 1 a ganado la ronda")
        elif winner_number == player2_price:
            player2_score += win_score
            player1_score += lost_score
            speak_and_print("Jugador 2 a ganado la ronda")

        image_src, product_name, final_price = get_random_product_attributes(session, coolmod_categories)
        game_rounds += 1

    if player1_score > player2_score:
        speak_and_print("El jugador 1 a ganado la partida, felicidades")

    elif player2_score > player1_score:
        speak_and_print("El jugador 2 a ganado la partida, felicidades")


def closest_number(players_list, final_price):
    return min(players_list[-1], key=lambda x: abs(x-final_price))


def speak_and_print(phrase, *args):
    if args:
        for a in args:
            print(phrase.format(a))
            speak(phrase.format(a))
    else:
        print(phrase)
        speak(phrase)


def main():
    # Unfinished code
    # Test git
    # Test git 2
    session = HTMLSession()

    speak_and_print("Bienvenido al precio justo, vamos a intentar adivinar los precios de algunos productos")

    coolmod_categories = get_coolmod_select_category(session)
    image_src, product_name, final_price = get_random_product_attributes(session, coolmod_categories)

    start_game(session, coolmod_categories, image_src, product_name, final_price)


if __name__ == "__main__":
    main()
