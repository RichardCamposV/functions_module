import re
import PySimpleGUI as sg

PLAYER_ONE = "X"
PLAYER_TWO = "O"


def player_type_win(player_one_list, player_two_list, type_win):
    if player_one_list == type_win:
        return False, "Jugador 1 a ganado!!!"
    elif player_two_list == type_win:
        return False, "Jugador 2 a ganado!!!"
    return True, ""


def check_game_won_nate(event, current_player, deck):
    winner_plays = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]

    index = int(event.replace("-", ""))
    deck[index] = current_player

    for winner_play in winner_plays:
        if deck[winner_play[0]] == deck[winner_play[1]] == deck[winner_play[2]] != 0:
            if deck[winner_play[0]] == PLAYER_ONE:
                return False, "El jugador 1 ha ganado!!!"
            elif deck[winner_play[0]] == PLAYER_TWO:
                return False, "El jugador 2 ha ganado!!!"

    if 0 not in deck:
        return False, "Juego terminado!"
    return True, ""


def check_game_won_rcv(layout):
    symbol_one = "X"
    symbol_two = "O"
    diagonal_win = [0, 0, 0]
    vertical_and_horizontal_win = [[0, 1, 0], [1, 0, 1]]
    player_one_list = []
    player_two_list = []

    for section in layout:
        for data in section:
            if data.Type == "button":
                if data.ButtonText == symbol_one:
                    position = re.findall("-([0-9])-", data.Key)
                    if len(position) != 0:
                        player_one_list.append((int(position[0]) % 2))
                elif data.ButtonText == symbol_two:
                    position = re.findall("-([0-9])-", data.Key)
                    if len(position) != 0:
                        player_two_list.append((int(position[0]) % 2))
    # Diagonal method
    game_check, player_winner = player_type_win(player_one_list, player_two_list, diagonal_win)
    # Vertical and horizontal method
    if game_check:
        for type_win in vertical_and_horizontal_win:
            game_check, player_winner = player_type_win(player_one_list, player_two_list, type_win)
            if not game_check:
                return game_check, player_winner

    return game_check, player_winner


def layout_game(button_size):
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
        [sg.Text("", key="-WINNER-", justification="center")],
        [sg.Button("Cerrar", key="-OK-")]]
    return layout


def main():
    game_active = True
    button_size = (7, 3)
    current_player = PLAYER_ONE

    deck = [0, 0, 0,
            0, 0, 0,
            0, 0, 0]

    layout = layout_game(button_size)
    window = sg.Window("Demo", layout)

    while game_active:
        event, value = window.read()
        if event == sg.WINDOW_CLOSED or event == "-OK-":
            break
        if window.Element(event).ButtonText == "":
            window.Element(event).Update(text=current_player)

            game_active, player_winner = check_game_won_nate(event, current_player, deck)
            window["-WINNER-"].update(player_winner)
            if current_player == PLAYER_ONE:
                current_player = PLAYER_TWO
            elif current_player == PLAYER_TWO:
                current_player = PLAYER_ONE
        # game_active, player_winner = check_game_won_rcv(layout)
    window.read()
    window.close()


if __name__ == "__main__":
    main()
