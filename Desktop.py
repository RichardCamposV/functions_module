import re
import PySimpleGUI as sg

PLAYER_ONE = "X"
PLAYER_TWO = "O"


def player_type_win(player_one_list, player_two_list, type_win):
    if player_one_list == type_win:
        print("Jugador 1 a ganado")
        return False
    elif player_two_list == type_win:
        print("Jugador 2 a ganado")
        return False
    return True


def check_game_won_rcv(layout):
    symbol_one = "X"
    symbol_two = "O"
    diagonal_win = [0, 0, 0]
    vertical_and_horizontal_win = [[0, 1, 0], [1, 0, 1]]
    player_one_list = []
    player_two_list = []

    for section in layout:
        for data in section:
            if data.ButtonText == symbol_one:
                position = re.findall("-([0-9])-", data.Key)
                if len(position) != 0:
                    player_one_list.append((int(position[0]) % 2))
            elif data.ButtonText == symbol_two:
                position = re.findall("-([0-9])-", data.Key)
                if len(position) != 0:
                    player_two_list.append((int(position[0]) % 2))
    # Diagonal method
    game_check = player_type_win(player_one_list, player_two_list, diagonal_win)
    # Vertical and horizontal method
    if game_check:
        for type_win in vertical_and_horizontal_win:
            game_check = player_type_win(player_one_list, player_two_list, type_win)
            if not game_check:
                return game_check

    return game_check


def main():
    game_active = True
    button_size = (7, 3)

    current_player = PLAYER_ONE

    layout = [[
                 sg.Button("", key="-0-", size=button_size),
                 sg.Button("", key="-1-", size=button_size),
                 sg.Button("", key="-2-", size=button_size)],
              [
                 sg.Button("", key="-3-", size=button_size),
                 sg.Button("", key="-4-", size=button_size),
                 sg.Button("", key="-5-", size=button_size)
              ],
              [
                 sg.Button("", key="-6-", size=button_size),
                 sg.Button("", key="-7-", size=button_size),
                 sg.Button("", key="-8-", size=button_size)
              ],
              [sg.Button("Cerrar", key="-OK-")]]

    window = sg.Window("Demo", layout)

    while game_active:
        event, value = window.read()
        if event == sg.WINDOW_CLOSED or event == "-OK-":
            break
        if window.Element(event).ButtonText == "":
            window.Element(event).Update(text=current_player)
            if current_player == PLAYER_ONE:
                current_player = PLAYER_TWO
            elif current_player == PLAYER_TWO:
                current_player = PLAYER_ONE
        game_active = check_game_won_rcv(layout)

    window.close()


if __name__ == "__main__":
    main()
