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
            speak("Con que categorias le gustaria jugar")
            user_category = hear_me()
            for data in list_categories:
                if user_category.lower() in data:
                    if len(select_user_categories) < 1:
                        select_user_categories.append(data)
                        print("Se agrego: {}, a la lista de juego".format(data[0]))
                        speak("Se agrego {} a la lista de juego".format(data[0]))
                    elif len(select_user_categories) >= 1:
                        category_exist = False
                        for category in select_user_categories:
                            if user_category.lower() in category:
                                category_exist = True
                                print("Ya existe: {}, en la lista de juego".format(category[0]))
                                speak("Ya existe {} en la lista de juego".format(category[0]))
                        if not category_exist:
                            select_user_categories.append(data)
                            print("Se agrego: {}, a la lista de juego".format(data[0]))
                            speak("Se agrego {} a la lista de juego".format(data[0]))
        else:
            user_select = True

    return select_user_categories


def get_random_product_attributes(session, categories):
    product_page_url = random.choice(categories)
    print("\nLa categoria con la que jugaremos sera: {}".format(product_page_url[0]))
    speak("La categoria con la que jugaremos sera {}".format(product_page_url[0]))

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


def main():
    session = HTMLSession()

    speak("Bienvenido al precio justo, vamos a intentar adivinar los precios de algunos productos")

    coolmod_categories = get_coolmod_select_category(session)
    image_src, product_name, final_price = get_random_product_attributes(session, coolmod_categories)

    show_image(session, image_src)

    print(product_name)
    speak("El nombre del producto es {}, cuanto crees que vale?".format(product_name))

    user_guess = hear_price_and_get_price()
    speak("El precio era {}".format(final_price))
    print(final_price)


if __name__ == "__main__":
    main()
