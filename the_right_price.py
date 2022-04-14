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
            price.replace(" euros", "").replace(",", ".").replace(" with ", ".")
            final_price = float(price)
            print(final_price)
            return final_price
        except ValueError:
            speak("No he entendido el numero")


def get_coolmod_categories(session):
    main_site = session.get(COOLMOD_URL)
    return main_site.html.find(".subfamilyheadertittle")


def get_random_product_attributes(session, categories):
    category = random.choice(categories)

    while category.text == "Configura tu PC a Medida":
        category = random.choice(categories)

    product_page_url = None
    for link_product in category.absolute_links:
        product_page_url = link_product

    product_page = session.get(product_page_url)
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

    coolmod_categories = get_coolmod_categories(session)
    image_src, product_name, final_price = get_random_product_attributes(session, coolmod_categories)

    show_image(session, image_src)

    print(product_name)
    speak("El nombre del producto es {}, cuanto crees que vale?".format(product_name))

    user_guess = hear_price_and_get_price()
    speak("El precio era {}".format(final_price))
    print(final_price)


if __name__ == "__main__":
    main()
