from time import sleep
from requests_html import HTMLSession
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


def temp_request(url, button_to_check):
    session = HTMLSession()
    product_page = session.get(url)
    found = product_page.html.find("{}".format(button_to_check))
    return found


def search_and_click(driver, word, type_element):
    if type_element == "id":
        return driver.find_element(By.ID, "{}".format(word)).click()
    elif type_element == "cn":
        return driver.find_element(By.CLASS_NAME, "{}".format(word)).click()
    elif type_element == "name":
        return driver.find_element(By.NAME, "{}".format(word)).click()
    else:
        print("Ningun tipo de elemento valido se a pasado...")


def check_status():
    url = "https://www.digitalife.com.mx/productos/memoria-ram-ddr4-hyperx-predator-8gb-4000mhz-135v-c19-negro"
    button_to_check = "#section-3e13b150-ad9c-11ec-a9ef-15e8d0d95d5e"

    buy_zone = temp_request(url, button_to_check)
    print(buy_zone)


def cyberpuerta_stock():
    pass


def coolmod_stock():
    url = "https://www.coolmod.com/zotac-gaming-geforce-rtx-3090-arcticstorm-24gb-gddr6x-tarjeta-grafica/"
    button_to_check = "#productbuybutton1"

    buy_zone = temp_request(url, button_to_check)

    if len(buy_zone) > 0:
        driver = webdriver.Firefox()
        driver.maximize_window()
        driver.get(url)
        # Nate Method:
        # driver.find_element_by_class_name("button coolprimarybutton px-3 py-1 mt-1").click()
        search_and_click(driver, "fas.fa-times-circle", "cn")
        search_and_click(driver, "button.coolprimarybutton.px-3.py-1.mt-1", "cn")
        search_and_click(driver, "button.coolprimarybutton.m-0.w-100.h-100", "cn")
        search_and_click(driver, "buybuttonproductcolor.h-100.text-center.d-block.w-100.position-relative.button.coolprimarybutton", "cn")
        sleep(1)
        search_and_click(driver, "swal2-confirm.swal2-styled", "cn")
        sleep(3)
        search_and_click(driver, "button.d-block.py-2.text-center.summaryheader.w-100.coolprimarybutton", "cn")

        is_form_loaded = False
        form = None

        while not is_form_loaded:
            try:
                form = search_and_click(driver, "underlineinput", "cn")
                is_form_loaded = True
            except NoSuchElementException:
                print("Puesssss no esta el formulario...")
                sleep(1)

        sleep(5)
        email = form.find_element(By.NAME, "inputEmail")
        password = form.find_element(By.NAME, "inputPassword")

        email.send_keys("ricard@ricard.com")
        password.send_keys("megustarazer")

        search_and_click(driver, "sendlogin.button", "cn")


def pc_componentes_stock():
    url = "https://www.pccomponentes.com/asus-geforce-gtx-1050-tis-4gb-gddr5"
    button_to_check = "#btnsWishAddBuy"

    while True:
        buy_zone = temp_request(url, button_to_check)
        if len(buy_zone) > 0:
            print("HAY STOCK!!!")
            break
        else:
            print("Sigue sin haber stock :(")
        sleep(30)


def main():

    # Load the page we want to check item stock
    # pc_componentes_stock()
    # check_status()
    coolmod_stock()


if __name__ == "__main__":
    main()
