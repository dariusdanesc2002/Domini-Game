import random


def create_dominos_set():
    dominos_set = list()
    for i in range(7):
        for j in range(i, 7):
            dominos_piece = list()
            dominos_piece.append(i)
            dominos_piece.append(j)
            dominos_set.append(dominos_piece)

    return dominos_set


def share_dominos_piece(dominos_set):
    dominos_shaerd = list()
    for i in range(7):
        number = random.randint(0, len(dominos_set) - 1)
        dominos_shaerd.append(dominos_set.pop(number))
    return dominos_shaerd


def verify_pieces(player_pieces):
    for pair in player_pieces:
        if pair[0] == pair[1]:
            return 1
    return 0


def determinate_begining_snake(player_pieces, computer_pieces):
    max_player_pieces = list()
    max_computer_pieces = list()
    for pair in player_pieces:
        if pair[0] == pair[1] and pair > max_player_pieces:
            max_player_pieces = pair
    for pair in computer_pieces:
        if pair[0] == pair[1] and pair > max_computer_pieces:
            max_computer_pieces = pair
    if max_player_pieces > max_computer_pieces:
        player_pieces.pop(player_pieces.index(max_player_pieces))
        return max_player_pieces
    else:
        computer_pieces.pop(computer_pieces.index(max_computer_pieces))
        return max_computer_pieces


def determinate_status(player_pieces, computer_pieces):
    max_player_pieces = list()
    max_computer_pieces = list()
    for pair in player_pieces:
        if pair[0] == pair[1] and pair > max_player_pieces:
            max_player_pieces = pair
    for pair in computer_pieces:
        if pair[0] == pair[1] and pair > max_computer_pieces:
            max_computer_pieces = pair
    if max_player_pieces > max_computer_pieces:
        return "computer"
    else:
        return "player"


def identical_snake(snake, counter):
    for index_counter, pair_counter in enumerate(counter):
        if pair_counter[0] == 8:
            for pair_snake in snake:
                if pair_snake[0] == index_counter and snake[pair_counter[1]][1] == index_counter:
                    return True
    return False


def game_still_running(snake, counter, player_pieces, computer_pieces):
    if identical_snake(snake, counter) == False and len(player_pieces) > 0 and len(computer_pieces) > 0:
        return True
    else:
        return False


def print_snake(snake):
    if len(snake) <= 6:
        for piece in snake:
            print(piece, end="")

    else:
        print(f"{snake[0]}{snake[1]}{snake[2]}...{snake[-3]}{snake[-2]}{snake[-1]}")


def verify_number(number, player_pieces):
    if len(player_pieces) >= int(number) >= -len(player_pieces) and number.isdigit():
        return True
    else:
        return False


def place_piece_in_snake(snake, number, player, dominos_set, counter):
    number = int(number)
    if number > 0:
        if snake[len(snake) - 1][1] == player[number - 1][0]:
            snake.append(player[number - 1])
        else:
            swap = player[number - 1][0]
            player[number - 1][0] = player[number - 1][1]
            player[number - 1][1] = swap
            snake.append(player[number - 1])

        counter[player[number - 1][0]][0] += 1
        counter[player[number - 1][1]][0] += 1
        counter[player[number - 1][0]][1] = len(snake)
        counter[player[number - 1][1]][1] = len(snake)
        player.remove(player[number - 1])
    if number < 0:
        snake.insert(0, player[-(number + 1)])
        counter[player[-(number + 1)][0]][0] += 1
        counter[player[-(number + 1)][1]][0] += 1
        counter[player[-(number + 1)][0]][1] = len(snake)
        counter[player[-(number + 1)][1]][1] = len(snake)
        player.remove(player[-(number + 1)])
    if number == 0 and len(dominos_set) > 0:
        index = random.randint(0, len(dominos_set) - 1)
        player.append(dominos_set[index])
        dominos_set.remove(dominos_set[index])


def verify_move(snake, number, player):
    number = int(number)
    if number > 0:
        if snake[len(snake) - 1][0] == player[number - 1][0] or snake[len(snake) - 1][0] == player[number - 1][1] or \
                snake[len(snake) - 1][1] == player[number - 1][0] or snake[len(snake) - 1][1] == player[number - 1][1]:
            return True
        else:
            return False
    if number < 0:
        if snake[0][0] == player[number - 1][0] or snake[0][0] == player[number - 1][1]:
            return True
        else:
            return False

    return True


def counting(computer_pieces, snake, computer):
    for list in computer_pieces:
        for pair in list:
            computer[pair] = computer[pair] + 1
    for list in snake:
        for pair in list:
            computer[pair] = computer[pair] + 1


def number_for_AI(computer, snake, computer_pieces, dominos_set, counter):
    sum = 0
    c = 1
    vector = []
    for piece in computer_pieces:
        sum = computer[piece[0]] + computer[piece[1]]
        mini_vector = [c, sum]
        vector.append(mini_vector)
        sum = 0
        c = c + 1
    vector_sortat = sorted(vector, key=lambda x: x[1], reverse=True)

    for piece in vector_sortat:
        if verify_move(snake, piece[0], computer_pieces) == True:
            place_piece_in_snake(snake,piece[0],computer_pieces, dominos_set, counter)
            break
        if verify_move(snake, -piece[0], computer_pieces) == True:
            place_piece_in_snake(snake,-piece[0],computer_pieces, dominos_set, counter)
            break
        place_piece_in_snake(snake, 0, computer_pieces, dominos_set, counter)


if __name__ == '__main__':
    dominos_set = create_dominos_set()
    player_pieces = list()
    computer_pieces = list()
    counter = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

    while verify_pieces(player_pieces) + verify_pieces(computer_pieces) < 1:
        player_pieces = share_dominos_piece(dominos_set)
        computer_pieces = share_dominos_piece(dominos_set)

    status = determinate_status(player_pieces, computer_pieces)
    snake = determinate_begining_snake(player_pieces, computer_pieces)
    snake = [snake]

    # print("Stock pieces : {stock}".format(stock=dominos_set))
    # print("Computer pieces: {Computer}".format(Computer=computer_pieces))
    # print("Player pieces: {Player}".format(Player=player_pieces))
    # print("Domino snake: {snake}".format(snake=snake))
    # print("Status: {status}".format(status=status))

    computer = [int(0) for num in range(0,7)]


    while game_still_running(snake, counter, player_pieces, computer_pieces):
        if status == "player":
            print("======================================================================")
            print("Stock size: {size}".format(size=len(dominos_set)))
            print("Computer pieces: {size}".format(size=len(computer_pieces)))
            print()
            print_snake(snake)
            print()
            print()
            print("Your pieces:")
            for pair in player_pieces:
                print("{index}:{pair}".format(index=player_pieces.index(pair) + 1, pair=pair))
            print()
            print("Status: It's your turn to make a move. Enter your command.")
            number = input()
            while not verify_number(number, player_pieces):
                print("Invalid input. Please try again.")
                number = input()
            while not verify_move(snake, number, player_pieces):
                print("Illegal move. Please try again.")
                number = input()
            place_piece_in_snake(snake, number, player_pieces, dominos_set, counter)
            if len(player_pieces) == 0:
                print("Your pieces:")
                print()
                print("Status: The game is over. You won!")
            status = "computer"

        else:
            print("======================================================================")
            print("Stock size: {size}".format(size=len(dominos_set)))
            print("Computer pieces: {size}".format(size=len(computer_pieces)))
            print()
            print_snake(snake)
            print()
            print()
            print("Your pieces:")
            for pair in player_pieces:
                print("{index}:{pair}".format(index=player_pieces.index(pair) + 1, pair=pair))
            # number = random.randint(-len(computer_pieces) + 1, len(computer_pieces) - 1)
            # while not verify_move(snake, number, computer_pieces):
            #     number = random.randint(-len(computer_pieces) + 1, len(computer_pieces) - 1)
            counting(computer_pieces, snake, computer)
            number_for_AI(computer, snake, computer_pieces, dominos_set, counter)
            computer = [int(0) for num in range(0, 7)]
            print()
            input("Status: Computer is about to make a move. Press Enter to continue...")
            if len(computer_pieces) == 0:
                print("Your pieces:")
                print()
                print("Status: The game is over. The computer won!")
            status = "player"
