import random
import copy
import statistics
import DataAnalysis as da


def check_bounds(position):
    column = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10}
    row = {"0": 1, "1": 2, "2": 3, "3": 4, "4": 5, "5": 6, "6": 7, "7": 8, "8": 9, "9": 10}
    if position[0] not in column.keys() or position[1] not in row.keys():
        return False
    else:
        return True


def convert_position(position):
    column = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10}
    row = {"0": 1, "1": 2, "2": 3, "3": 4, "4": 5, "5": 6, "6": 7, "7": 8, "8": 9, "9": 10}
    r = row[position[1]]
    c = column[position[0]]
    return r, c


def convert_coord(rowpos, columnpos):
    column = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9, "J": 10}
    row = {"0": 1, "1": 2, "2": 3, "3": 4, "4": 5, "5": 6, "6": 7, "7": 8, "8": 9, "9": 10}
    firstpart = ""
    secondpart = ""
    for key, value in column.items():
        if value == columnpos:
            firstpart = key
    for key, value in row.items():
        if value == rowpos:
            secondpart = key
    if len(firstpart + secondpart) != 2:
        return False
    return firstpart + secondpart


def end_game(player1, player2):
    if player1.enemyboats == {}:
        print(player1.name, " has won")
        return 1
    elif player2.enemyboats == {}:
        print(player2.name, " has won")
        return 2
    return False


def find_max(lista):
    max_value = 0
    max_index = []
    for row_idx, row in enumerate(lista):
        for col_idx, col in enumerate(row):
            if col > max_value:
                max_value = col
                max_index = [(row_idx, col_idx)]
            elif col == max_value:
                x = (row_idx, col_idx)
                max_index.append(x)
    return max_index


def initial_probability():
    b = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    z = {5, 4, 3, 2, 3}
    for r in range(0, 5):
        for c in range(r, 5):
            left = min(c + 1, 5)
            right = min(9 - c, 5)
            up = min(r + 1, 5)
            down = min(9 - r, 5)
            b[r][c] = left * right + up * down
            for i in z:
                if max(left, right) < i <= left + right - 1:
                    b[r][c] += (left + right) - i
            for i in z:
                if max(up, down) < i <= up + down - 1:
                    b[r][c] += (up + down) - i
            if min(left, right) < 3:
                pass
            elif min(left, right) == 3:
                b[r][c] = b[r][c] - 1
            elif min(left, right) == 4:
                b[r][c] -= 4
            elif min(left, right) == 5:
                b[r][c] -= 8
            if min(up, down) < 3:
                pass
            elif min(up, down) == 3:
                b[r][c] = b[r][c] - 1
            elif min(up, down) == 4:
                b[r][c] -= 4
            elif min(up, down) == 5:
                b[r][c] -= 8
    for r in range(0, 5):
        for c in range(0, 5):
            b[c][r] = b[r][c]
            b[r][9 - c] = b[r][c]
            b[9 - r][c] = b[r][c]
            b[9 - r][9 - c] = b[r][c]
    return b


def get_prob(numberOfShipsLeft, spaceDirection1, spaceDirection2):
    a = [i for i in numberOfShipsLeft if i <= max(spaceDirection1, spaceDirection2)]
    if len(a) == max(a):
        probability = min(max(a), spaceDirection1) * min(max(a), spaceDirection2)


class Board(object):

    def __init__(self, name):
        """
        get the blank board and sets the name and guess dictionary
        :param name:
        """
        self.map = [[" ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                    ["0", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                    ["1", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                    ["2", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                    ["3", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                    ["4", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                    ["5", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                    ["6", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                    ["7", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                    ["8", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                    ["9", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']]
        self.guessing_map = [[" ", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
                             ["0", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                             ["1", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                             ["2", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                             ["3", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                             ["4", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                             ["5", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                             ["6", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                             ["7", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                             ["8", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0'],
                             ["9", '0', '0', '0', '0', '0', '0', '0', '0', '0', '0']]
        self.name = name
        self.guesses = []
        self.boats = {5: [], 4: [], 3: [[], []], 2: []}
        self.enemyboats = {}
        self.enemyboats1 = {}

    def print_board(self, dic):
        """
        will print the board into a nice board. really need to look at how bigger boards will affect it
        also need to see how the different letters will affect it
        :return:
        """
        for row in range(len(dic)):
            print(" ".join(dic[row]))

    def add_guesses(self, guess):
        """
        adds the stuff to guess dictionary
        :param guess: should be a tuple with the first being the coordinate and then whether it is a hit or miss
        :return:
        """
        self.guesses.append(guess[0])
        self.guesses.append(guess[1])
        pos = convert_position(guess[0])
        self.guessing_map[pos[0]][pos[1]] = guess[1]

    def check_guess(self, guess, guessing_board):
        """

        :param guess: should be a string of two characters
        :param guessing_board: the other player. should be of class board so that can call .map
        :return: returns true if it is a valid guess. if the guess is not of the board or has already been guessed it is false
        """
        xypos = convert_position(guess)
        if not check_bounds(guess):
            print("ERROR BOUNDS")
            return False
        elif guess in self.guesses:
            print("ERROR IN GUESSES")
            return False
        else:
            if guessing_board.map[xypos[0]][xypos[1]] == "X":
                result = (guess, "H")
                for k, v in self.enemyboats.items():
                    if k == 3 and len(self.enemyboats[3]) == 2:
                        if guess in v[0]:
                            v[0].remove(guess)
                        elif guess in v[1]:
                            v[1].remove(guess)
                    elif k == 3:
                        if guess in v[0]:
                            v[0].remove(guess)
                    else:
                        if guess in v:
                            v.remove(guess)
            else:
                result = (guess, "M")
            self.add_guesses(result)
            return result

    def check_place_battleship(self, start_position, end_position, length):
        """
        Checks to see if the battleship is a valid placement of a ship
        1) is whether the start/end pos are even on the board
        2) checks whether boats is a column or row. doesnt tell you which but makes sure there isnt a diagonal
        3) checks to see if distance between the start and end pos match the given length
        4) checks to see if any of the points that would make up the battleship are already selected
        5) places the battleship in both boats and on the board with a mark of "X"
        :param start_position: should be a string
        :param end_position: should be a string
        :param length: should be an int either 5,4,3,2
        :return: boolean about whether it is a valid placement or not
        """
        if not check_bounds(start_position) or not check_bounds(end_position):
            # print("Not in Bounds")
            return False
        if start_position[0] != end_position[0] and start_position[1] != end_position[1]:
            # print("Columns or rows don't match")
            return False
        xystartpos = convert_position(start_position)
        xyendpos = convert_position(end_position)
        if abs(xyendpos[0] - xystartpos[0]) + 1 != length and abs(xyendpos[1] - xystartpos[1]) + 1 != length:
            # print("incorrect length")
            return False
        pos = []
        if xyendpos[0] == xystartpos[0]:
            for ypos in range(xystartpos[1], xyendpos[1] + 1):
                position = convert_coord(xystartpos[0], ypos)
                if position in [x for v in self.boats.values() for x in v] or position in [x for v in self.boats[3] for
                                                                                           x in v]:
                    # print("Already selected")
                    return False
                if length == 3:
                    if len(self.boats[length][0]) == 3 and len(self.boats[length][1]) == 3:
                        # print("Already have ships of that length")
                        return False
                    elif len(self.boats[length][0]) != 3:
                        pos.append(position)
                    else:
                        pos.append(position)
                elif len(self.boats[length]) == length:
                    # print("Already have ships of that length")
                    return False
                else:
                    pos.append(position)
        else:
            for xpos in range(xystartpos[0], xyendpos[0] + 1):
                position = convert_coord(xpos, xystartpos[1])
                if position in [x for v in self.boats.values() for x in v] or position in [x for v in self.boats[3] for
                                                                                           x in v]:
                    # print("Already selected 1")
                    return False
                if length == 3:
                    if len(self.boats[length][0]) == 3 and len(self.boats[length][1]) == 3:
                        # print("Already have ships of that length 2")
                        return False
                    elif len(self.boats[length][0]) != 3:
                        pos.append(position)
                    else:
                        pos.append(position)
                elif len(self.boats[length]) == length:
                    # print("Already have ships of that length")
                    return False
                else:
                    pos.append(position)
        if length == 3:
            if len(self.boats[length][0]) != 3:
                for item in pos:
                    xypos = convert_position(item)
                    self.boats[length][0].append(item)
                    self.map[xypos[0]][xypos[1]] = "X"
            else:
                for item in pos:
                    xypos = convert_position(item)
                    self.boats[length][1].append(item)
                    self.map[xypos[0]][xypos[1]] = "X"
        else:
            for item in pos:
                xypos = convert_position(item)
                self.boats[length].append(item)
                self.map[xypos[0]][xypos[1]] = "X"
        return True

    def copy_guess(self, guessing_board):
        """
        copies the position of the boats from the opponent
        enemyboats is the one that gets changes will be used to check if the game is won
        :param guessing_board: should be of class board
        :return:
        """
        self.enemyboats = copy.deepcopy(guessing_board.boats)
        self.enemyboats1 = copy.deepcopy(guessing_board.boats)

    @property
    def check_sunk(self):
        """
        checks to see the boat is sunk and then will remove the boats from the length so that the boats will not keep
        triggering the boats
        :return:
        """
        for k, v in self.enemyboats.items():
            if k == 3 and len(self.enemyboats[k]) == 2:
                if len(v[0]) == 0:
                    del self.enemyboats[k][0]
                    return k
                if len(v[1]) == 0:
                    del self.enemyboats[k][1]
                    return k
            elif k == 3:
                if len(v[0]) == 0:
                    del self.enemyboats[k]
                    return k
            else:
                if len(self.enemyboats[k]) == 0:
                    del self.enemyboats[k]
                    return k
        return False

    def get_max_ship_length(self):
        return max(self.enemyboats.keys())

    def get_ships(self):
        ships = list(self.enemyboats)
        if 3 in ships:
            if len(self.enemyboats[3]) == 2:
                ships.append(3)
        return ships

    def get_min_ship_length(self):
        return min(self.enemyboats.keys())


class Human(Board):
    def checkboats(self):
        """
        checks to see if there are still more boats to be places
        :return:
        """
        for key in self.boats:
            if key == 3:
                if len(self.boats[key][0]) != 3 or len(self.boats[3][1]) != 3:
                    return False
            else:
                if len(self.boats[key]) != key:
                    return False
                else:
                    pass
        return True

    def placement(self):
        """
        asks for placement until all the boats are placed.
        :return:
        """
        while True:
            length = int(input("BattleShip Length: "))
            startpos = input("Starting position: ")
            endpos = input("Ending position: ")
            self.check_place_battleship(startpos, endpos, length)
            self.print_board(self.map)
            print(self.boats)
            if self.checkboats():
                break

    def play(self, opponent):
        """
        asks for input and then checks to make sure its valid
        :param opponent: of class board
        :return:
        """
        while True:
            guess = input("Guess: ")
            a = self.check_guess(guess, opponent)
            if a:
                if a[1] == "H":
                    print("Hit!")
                    b = self.check_sunk
                    if b:
                        print("Battleship sunk!")
                        break
                    break
                else:
                    print("Miss!")
                    break
            else:
                print("not a valid guess")


class Computer(Board):

    def __init__(self, name, difficulty):
        """
        first hit will be when a computer gets a hit and then once it moves if it encounters a miss it will go back to
            this guess and move in the other direction
        direction will be up/left/down/right
        hits stores every guess that was a hit and then will delete the hits that correspond to a sunk boat which allows
            for the computer to know if there are still boats left in the guess pool. especially helpful with the medium
            since that one skips steps
        :param name:
        :param difficulty: should be a string either easy or medium as of right now 8/22
        """
        super().__init__(name)
        self.firsthit = ""
        self.direction = 0
        self.difficulty = difficulty
        self.hits = []
        self.probability = initial_probability()

    def remove_sunk_hits(self, key1):
        """
        removes from the hits list the guesses that correspond to the sunk boats. really only for medium, maybe hard
            once i get that set up
        :param key1: will be taken from check sunk and should only ever be 5,4,3,2
        :return:
        """
        if key1 == 3:
            if all(elem in self.hits for elem in self.enemyboats1[3][0]):
                self.hits = [x for x in self.hits if x not in self.enemyboats1[3][0]]
            elif all(elem in self.hits for elem in self.enemyboats1[3][1]):
                self.hits = [x for x in self.hits if x not in self.enemyboats1[3][1]]
        else:
            self.hits = [x for x in self.hits if x not in self.enemyboats1[key1]]

    def change_sunk_hits(self, key):
        z = []
        if key == 3:
            if all(elem in self.hits for elem in self.enemyboats1[3][0]):
                z = [x for x in self.hits if x in self.enemyboats1[3][0]]
            elif all(elem in self.hits for elem in self.enemyboats1[3][1]):
                z = [x for x in self.hits if x in self.enemyboats1[3][1]]
        else:
            z = [x for x in self.hits if x in self.enemyboats1[key]]
        return z

    def guess(self, board):
        """
        depending on the difficulty will make an intial guess or after a battle ship has been sunk and needs a new
            starting guess
        easy just randomly guesses and medium will guess every other spot with each rows having even columns and odd rows
            having odd columns
        each runs the check guess and then if it is a hit will change the first hit and append the hits list
        :param board: should be the opponent of class board
        :return:
        """
        if self.difficulty == "easy":
            while True:
                row = random.randint(1, 10)
                column = random.randint(1, 10)
                coord = convert_coord(row, column)
                result = self.check_guess(coord, board)
                if result:
                    if result[1] == "H":
                        self.hits.append(result[0])
                        self.firsthit = result[0]
                    break
        elif self.difficulty == "medium":
            minkey = min(self.enemyboats.keys())
            while True:
                row = random.randint(1, 10)
                a = list(range(1, 11))
                columnchoice = list(filter(lambda x: (x % minkey == row % minkey), a))
                column = random.choice(columnchoice)
                coord = convert_coord(row, column)
                result = self.check_guess(coord, board)
                if result:
                    if result[1] == "H":
                        self.hits.append(result[0])
                        self.firsthit = result[0]
                    break
        return True

    def mastermode(self, opponent):
        maxpositions = find_max(self.probability)
        if len(maxpositions) > 1:
            choice = random.choice(maxpositions)
            guess = convert_coord(choice[0] + 1, choice[1] + 1)
            result = self.check_guess(guess, opponent)
            if result:
                if result[1] == "H":
                    self.hits.append(result[0])
                    q = self.check_sunk
                    if q:
                        u = self.change_sunk_hits(q)
                        self.remove_sunk_hits(q)
                        for item in u:
                            xypos = convert_position(item)
                            self.guessing_map[xypos[0]][xypos[1]] = "S"
                            self.probability[xypos[0] - 1][xypos[1] - 1] = 0
                        if len(self.enemyboats) == 0:
                            return 0
                        self.update_after_sink()
                    else:
                        self.probability[choice[0]][choice[1]] = -1
                        self.update_prob_hit(choice[0], choice[1])
                else:
                    self.probability[choice[0]][choice[1]] = 0
                    self.update_prob_miss(choice[0], choice[1])
            else:
                print("FAIL 1")
        else:
            guess = convert_coord(maxpositions[0][0] + 1, maxpositions[0][1] + 1)
            result = self.check_guess(guess, opponent)
            if result:
                if result[1] == "H":
                    self.hits.append(result[0])
                    q = self.check_sunk
                    if q:
                        u = self.change_sunk_hits(q)
                        self.remove_sunk_hits(q)
                        for item in u:
                            xypos = convert_position(item)
                            self.guessing_map[xypos[0]][xypos[1]] = "S"
                            self.probability[xypos[0] - 1][xypos[1] - 1] = 0
                        if len(self.enemyboats) == 0:
                            return 0
                        self.update_after_sink()
                    else:
                        self.probability[maxpositions[0][0]][maxpositions[0][1]] = -1
                        self.update_prob_hit(maxpositions[0][0], maxpositions[0][1])
                else:
                    self.probability[maxpositions[0][0]][maxpositions[0][1]] = 0
                    self.update_prob_miss(maxpositions[0][0], maxpositions[0][1])
            else:
                print("FAIL 2")

    def check_m(self, row, column):
        """
        the bounds are the amount of spaces til a bound. so (0,0) is 0 away (4,0) is 4 away
        :param row:
        :param column:
        :return:
        """
        bounds = []
        if 0 in self.probability[row][max(0, column - 4):column]:
            columnpos = [i for i, x in enumerate(self.probability[row][max(0, column - 4):column]) if x == 0]
            leftbound = (row, max(0, column - 4) + max(columnpos) + 1)
        else:
            leftbound = (row, max(0, column - 4))
        bounds.append(leftbound)
        if 0 in self.probability[row][column + 1:min(column + 4, 9) + 1]:
            columnpos = [i for i, x in enumerate(self.probability[row][column + 1:min(column + 4, 9) + 1]) if x == 0]
            rightbound = (row, column + min(columnpos))
        else:
            rightbound = (row, min(column + 4, 9))
        bounds.append(rightbound)
        upbound = (max(0, row - 4), column)
        for r in range(row - 1, max(0, row - 4) - 1, -1):
            if self.probability[r][column] == 0:
                upbound = (r + 1, column)
                break
        bounds.append(upbound)
        downbound = (min(row + 4, 9), column)
        for r in range(row + 1, min(row + 5, 10)):
            if self.probability[r][column] == 0:
                downbound = (r - 1, column)
                break
        bounds.append(downbound)
        return bounds

    def update_prob_miss(self, x, column):
        bounds = self.check_m(x, column)
        shipsLeft = self.get_ships()
        for c in range(column - 1, bounds[0][1] - 1, -1):
            if self.probability[x][c] == -1:
                bounds2 = self.check_m(x, c)
                closesthit = c
                mult = 1
                for y in range(c - 1, bounds2[0][1] - 1, -1):
                    if self.probability[x][y] == -1:
                        closesthit = y
                        mult += 1
                        continue
                    self.prob(x, y)
                    dis = abs(c - y)
                    count = sum(j == dis for j in shipsLeft)
                    self.probability[x][y] += count
                    if abs(closesthit - y) == 1:
                        self.probability[x][y] += 20 * mult
                    spacesameside = y - bounds2[0][1] + 1
                    count2 = sum(spacesameside + dis > j for j in shipsLeft)
                    spaceotherside = bounds2[1][1] - c + 1
                    count = sum(5 - j < spaceotherside and j > dis + 1 for j in shipsLeft)
                    self.probability[x][y] += count + count2
                break
            self.prob(x, c)
        for c in range(column + 1, bounds[1][1] + 1):
            if self.probability[x][c] == -1:
                bounds2 = self.check_m(x, c)
                closesthit = c
                mult = 1
                for y in range(c + 1, bounds2[1][1] + 1):
                    if self.probability[x][y] == -1:
                        closesthit = y
                        mult += 1
                        continue
                    self.prob(x, y)
                    dis = abs(c - y)
                    count = sum(j == dis for j in shipsLeft)
                    self.probability[x][y] += count
                    if abs(closesthit - y) == 1:
                        self.probability[x][y] += 20 * mult
                    spacesameside = bounds2[1][1] - y + 1
                    count2 = sum(spacesameside + dis > j for j in shipsLeft)
                    spaceotherside = c - bounds2[0][1] + 1
                    count = sum(5 - j < spaceotherside and j > dis + 1 for j in shipsLeft)
                    self.probability[x][y] += count + count2
                break
            self.prob(x, c)
        for r in range(x - 1, bounds[2][0] - 1, -1):
            if self.probability[r][column] == -1:
                bounds2 = self.check_m(r, column)
                closesthit = r
                mult = 1
                for z in range(r - 1, bounds2[2][0] - 1, -1):
                    if self.probability[z][column] == -1:
                        closesthit = z
                        mult += 1
                        continue
                    self.prob(z, column)
                    dis = abs(r - z)
                    count = sum(j > dis for j in shipsLeft)
                    self.probability[z][column] += count
                    if abs(closesthit - z) == 1:
                        self.probability[z][column] += 20 * mult
                    spacesameside = z - bounds2[2][0] + 1
                    count2 = sum(spacesameside + dis > j for j in shipsLeft)
                    spaceotherside = bounds2[3][0] - r + 1
                    count = sum(5 - j < spaceotherside and j > dis + 1 for j in shipsLeft)
                    self.probability[z][column] += count + count2
                break
            self.prob(r, column)
        for r in range(x + 1, bounds[3][0] + 1):
            if self.probability[r][column] == -1:
                bounds2 = self.check_m(r, column)
                closesthit = r
                mult = 1
                for z in range(r + 1, bounds2[3][0] + 1):
                    if self.probability[z][column] == -1:
                        closesthit = z
                        mult += 1
                        continue
                    self.prob(z, column)
                    dis = abs(r - z)
                    count = sum(j > dis for j in shipsLeft)
                    self.probability[z][column] += count
                    if abs(closesthit - z) == 1:
                        self.probability[z][column] += 20 * mult
                    spacesameside = bounds2[3][0] - z + 1
                    count2 = sum(spacesameside + dis > j for j in shipsLeft)
                    spaceotherside = r - bounds2[2][0] + 1
                    count = sum(5 - j < spaceotherside and j > dis + 1 for j in shipsLeft)
                    self.probability[z][column] += count + count2
                break
            self.prob(r, column)

    def update_after_sink(self):
        alreadyChecked = []
        shipsLeft = self.get_ships()
        for item in self.hits:
            if item in alreadyChecked:
                continue
            x, y = convert_position(item)
            x -= 1
            y -= 1
            bounds = self.check_m(x, y)
            mult = 1
            closesthit = y
            for c in range(y - 1, bounds[0][1] - 1, -1):
                if self.probability[x][c] == -1:
                    closesthit = c
                    mult += 1
                    continue
                self.probUD(x, c)
                dis = abs(y - c)
                count = sum(j > dis for j in shipsLeft)
                self.probability[x][c] += count
                if abs(closesthit - c) == 1:
                    self.probability[x][c] += 20 * mult
                spaceotherside = bounds[1][1] - y + 1
                count = sum(5 - j < spaceotherside and j > dis + 1 for j in shipsLeft)
                self.probability[x][c] += count
                alreadyChecked.append((x, c))
            closesthit = y
            mult = 1
            for c in range(y + 1, bounds[1][1] + 1):
                if self.probability[x][c] == -1:
                    closesthit = c
                    mult += 1
                    continue
                self.probUD(x, c)
                dis = abs(y - c)
                count = sum(j > dis for j in shipsLeft)
                self.probability[x][c] += count
                if abs(closesthit - c) == 1:
                    self.probability[x][c] += 20 * mult
                spaceotherside = y - bounds[0][1] + 1
                count = sum(5 - j < spaceotherside and j > dis + 1 for j in shipsLeft)
                self.probability[x][c] += count
                alreadyChecked.append((x, c))
            closesthit = x
            mult = 1
            for r in range(x - 1, bounds[2][0] - 1, -1):
                if self.probability[r][y] == -1:
                    closesthit = r
                    mult += 1
                    continue
                self.probLR(r, y)
                dis = abs(x - r)
                count = sum(j > dis for j in shipsLeft)
                self.probability[r][y] += count
                if abs(closesthit - r) == 1:
                    self.probability[r][y] += 20 * mult
                spaceotherside = bounds[3][0] - x + 1
                count = sum(5 - j < spaceotherside and j > dis + 1 for j in shipsLeft)
                self.probability[r][y] += count
                alreadyChecked.append((r, y))
            closesthit = x
            mult = 1
            for r in range(x + 1, bounds[3][0] + 1):
                if self.probability[r][y] == -1:
                    closesthit = r
                    mult += 1
                    continue
                self.probLR(r, y)
                dis = abs(x - r)
                count = sum(j > dis for j in shipsLeft)
                self.probability[r][y] += count
                if abs(closesthit - r) == 1:
                    self.probability[r][y] += 20 * mult
                spaceotherside = x - bounds[2][0] + 1
                count = sum(5 - j < spaceotherside and j > dis + 1 for j in shipsLeft)
                self.probability[r][y] += count
                alreadyChecked.append((r, y))
        for r in range(10):
            for c in range(10):
                if self.probability[r][c] == 0 or self.probability[r][c] == -1:
                    continue
                if (r, c) in alreadyChecked:
                    continue
                self.prob(r, c)

    def update_prob_hit(self, x, column):
        bounds = self.check_m(x, column)
        shipsLeft = self.get_ships()
        count2 = 0
        closesthit = column
        mult = 1
        for c in range(column - 1, bounds[0][1] - 1, -1):
            if self.probability[x][c] == -1:
                closesthit = c
                mult += 1
                continue
            dis = abs(column - c)
            count = sum(j == dis for j in shipsLeft)
            self.probability[x][c] += count
            if abs(closesthit - c) == 1:
                self.probability[x][c] += 20 * mult
            spacesameside = c - bounds[0][1] + 1
            count2 = sum(spacesameside + dis > j for j in shipsLeft)
            spaceotherside = bounds[1][1] - column + 1
            count = sum(5 - j < spaceotherside and j > dis + 1 for j in shipsLeft)
            self.probability[x][c] += count + count2
        closesthit = column
        mult = 1
        for c in range(column + 1, bounds[1][1] + 1):
            if self.probability[x][c] == -1:
                closesthit = c
                mult += 1
                continue
            dis = abs(column - c)
            count = sum(j == dis for j in shipsLeft)
            self.probability[x][c] += count
            if abs(closesthit - c) == 1:
                self.probability[x][c] += 20 * mult
            spacesameside = bounds[1][1] - c + 1
            count2 = sum(spacesameside + dis > j for j in shipsLeft)
            spaceotherside = column - bounds[0][1] + 1
            count = sum(5 - j < spaceotherside and j > dis + 1 for j in shipsLeft)
            self.probability[x][c] += count + count2
        closesthit = x
        mult = 1
        for r in range(x - 1, bounds[2][0] - 1, -1):
            if self.probability[r][column] == -1:
                closesthit = r
                mult += r
                continue
            dis = abs(x - r)
            count = sum(j > dis for j in shipsLeft)
            self.probability[r][column] += count
            if abs(closesthit - r) == 1:
                self.probability[r][column] += 20 * mult
            spacesameside = r - bounds[2][0] + 1
            count2 = sum(spacesameside + dis > j for j in shipsLeft)
            spaceotherside = bounds[3][0] - column + 1
            count = sum(5 - j < spaceotherside and j > dis + 1 for j in shipsLeft)
            self.probability[r][column] += count + count2
        closesthit = x
        mult = 1
        for r in range(x + 1, bounds[3][0] + 1):
            if self.probability[r][column] == -1:
                closesthit = r
                mult += r
                continue
            dis = abs(x - r)
            count = sum(j > dis for j in shipsLeft)
            self.probability[r][column] += count
            if abs(closesthit - r) == 1:
                self.probability[r][column] += 20 * mult
            spacesameside = bounds[3][0] - r + 1
            count2 = sum(spacesameside + dis > j for j in shipsLeft)
            spaceotherside = x - bounds[2][0] + 1
            count = sum(5 - j < spaceotherside and j > dis + 1 for j in shipsLeft)
            self.probability[r][column] += count + count2

    def probUD(self, row, column):
        bounds = self.check_m(row, column)
        maxLength = self.get_max_ship_length()
        up = row - bounds[2][0] + 1
        up = min(up, maxLength)
        down = bounds[3][0] - row + 1
        down = min(down, maxLength)
        ud = up * down
        if max(up, down) == 2 and min(up, down) == 1:
            ud = 1
        elif up == down == 2:
            ud = 2
        self.probability[row][column] = ud
        shipsLeft = self.get_ships()
        for i in shipsLeft:
            if max(up, down) < i <= up + down - 1:
                self.probability[row][column] += (up + down) - i
        if min(up, down) < 3:
            pass
        elif min(up, down) == 3:
            self.probability[row][column] -= 1
        elif min(up, down) == 4:
            self.probability[row][column] -= 4
        elif min(up, down) == 5:
            self.probability[row][column] -= 8
        for i in range(2, max(up, down) + 1):
            if i not in shipsLeft:
                self.probability[row][column] -= min(i, min(up, down))
                if i == 3:
                    self.probability[row][column] -= min(i, min(up, down))
            if i == 3 and shipsLeft.count(i) == 1:
                self.probability[row][column] -= min(i, min(up, down))

    def probLR(self, row, column):
        bounds = self.check_m(row, column)
        maxLength = self.get_max_ship_length()
        left = column - bounds[0][1] + 1
        left = min(left, maxLength)
        right = bounds[1][1] - column + 1
        right = min(right, maxLength)
        lr = left * right
        if max(left, right) == 2 and min(left, right) == 1:
            lr = 1
        elif left == 2 == right:
            lr = 2
        self.probability[row][column] = lr
        shipsLeft = self.get_ships()
        for i in shipsLeft:
            if max(left, right) < i <= left + right - 1:
                self.probability[row][column] += (left + right) - i
        if min(left, right) < 3:
            pass
        elif min(left, right) == 3:
            self.probability[row][column] -= 1
        elif min(left, right) == 4:
            self.probability[row][column] -= 4
        elif min(left, right) == 5:
            self.probability[row][column] -= 8
        for i in range(2, max(left, right) + 1):
            if i not in shipsLeft:
                self.probability[row][column] -= min(i, min(left, right))
                if i == 3:
                    self.probability[row][column] -= min(i, min(left, right))
            if i == 3 and shipsLeft.count(i) == 1:
                self.probability[row][column] -= min(i, min(left, right))

    def prob(self, x, column):
        bounds = self.check_m(x, column)
        maxLength = self.get_max_ship_length()
        left = column - bounds[0][1] + 1
        left = min(left, maxLength)
        right = bounds[1][1] - column + 1
        right = min(right, maxLength)
        up = x - bounds[2][0] + 1
        up = min(up, maxLength)
        down = bounds[3][0] - x + 1
        down = min(down, maxLength)
        lr = left * right
        ud = up * down
        if max(left, right) == 2 and min(left, right) == 1:
            lr = 1
        elif left == 2 == right:
            lr = 2
        if max(up, down) == 2 and min(up, down) == 1:
            ud = 1
        elif up == down == 2:
            ud = 2
        if left == 1 and right == 1:
            lr = 0
        if up == 1 and down == 1:
            ud = 0
        if lr == ud == 0:
            self.probability[x][column] = 0
            return 0
        self.probability[x][column] = lr + ud
        shipsLeft = self.get_ships()
        for i in shipsLeft:
            if max(left, right) < i <= left + right - 1:
                self.probability[x][column] += (left + right) - i
        for i in shipsLeft:
            if max(up, down) < i <= up + down - 1:
                self.probability[x][column] += (up + down) - i
        if min(left, right) < 3:
            pass
        elif min(left, right) == 3:
            self.probability[x][column] -= 1
        elif min(left, right) == 4:
            self.probability[x][column] -= 4
        elif min(left, right) == 5:
            self.probability[x][column] -= 8
        for i in range(2, max(left, right) + 1):
            if i not in shipsLeft:
                self.probability[x][column] -= min(i, min(left, right))
                if i == 3:
                    self.probability[x][column] -= min(i, min(left, right))
            if i == 3 and shipsLeft.count(i) == 1:
                self.probability[x][column] -= min(i, min(left, right))
        if min(up, down) < 3:
            pass
        elif min(up, down) == 3:
            self.probability[x][column] -= 1
        elif min(up, down) == 4:
            self.probability[x][column] -= 4
        elif min(up, down) == 5:
            self.probability[x][column] -= 8
        for i in range(2, max(up, down) + 1):
            if i not in shipsLeft:
                self.probability[x][column] -= min(i, min(up, down))
                if i == 3:
                    self.probability[x][column] -= min(i, min(up, down))
            if i == 3 and shipsLeft.count(i) == 1:
                self.probability[x][column] -= min(i, min(up, down))

    def afterguess(self, lastguess, result, board):
        """
        1) checks if the previous result was a hit or if it was a miss but there were hits before that guess
            a) checks to see if the direction has already been set. if not will randomly select 1-4
            b) checks to see if the direction isn't zero and the previous guess was a miss. if so will go back to the
                first hit and choose a new direction with which to go. probably could change it so that it will flip the
                direction
            c) checks to see if the direction is zero and if the first hit isnt blank. this means that there was a sunk
                ship but also other hits that haven't been completed yet
            d) stores the converted position from last guess in and x and y so that it can be manipulated if needed.
                counter is initialized so don't get stuck in an endless loop
            e) for rollfour 1 is right 2 is left 3 is down 4 is up
            f) will check if the guess is valid and then based on if it is a hit or miss it will add them
                1) if guess not in the guesses. it will add and if its a hit it will add to appropiate ones anc change
                    direction if its a miss it will change the direction
                2) if guess is in guesses and a hit it will move the the pos to that space so that it can hop more spaces
                    useful when starting at middle point. if miss it will rotate between the directions
                3) will rotate between the direction
            g) if the result was a miss it will do a new random guess
        :param lastguess: should be a two character string take from the self.guesses function
        :param result: either "h"" or "m" taken from the self.guesses function
        :param board: opponent of class board
        :return:
        """
        if result == "H" or self.direction != 0:
            if self.direction == 0:
                rollfour = random.randint(1, 4)
            else:
                rollfour = self.direction
            if self.direction != 0 and result == "M":
                lastguess = self.firsthit
                if self.direction == 1:
                    self.direction = 2
                elif self.direction == 2:
                    self.direction = 1
                elif self.direction == 3:
                    self.direction = 4
                elif self.direction == 4:
                    self.direction = 3
            if self.direction == 0 and self.firsthit != "":
                lastguess = self.firsthit
            xypos = convert_position(lastguess)
            x = xypos[0]
            y = xypos[1]
            counter = 0
            while True:
                if rollfour == 1:
                    xposguess = x + 1
                    guess = convert_coord(xposguess, xypos[1])
                    if guess and guess not in self.guesses:
                        ans = self.check_guess(guess, board)
                        if ans[1] == "H":
                            self.hits.append(guess)
                            self.direction = rollfour
                        elif ans[1] == "M":
                            self.direction = 2
                        return True
                    elif guess in self.guesses:
                        posa = self.guesses.index(guess)
                        if self.guesses[posa + 1] == "H":
                            x = xposguess
                            self.direction = 1
                        else:
                            if self.direction == 0:
                                rollfour = 2
                            else:
                                xypos = convert_position(self.firsthit)
                                self.direction = 2
                                counter += 1
                    else:
                        if self.direction == 0:
                            rollfour = 2
                        else:
                            xypos = convert_position(self.firsthit)
                            self.direction = 2
                            counter += 1
                if rollfour == 2:
                    xposguess = x - 1
                    guess = convert_coord(xposguess, xypos[1])
                    if guess and guess not in self.guesses:
                        ans = self.check_guess(guess, board)
                        if ans[1] == "H":
                            self.hits.append(guess)
                            self.direction = rollfour
                        elif ans[1] == "M":
                            self.direction = 1
                        return True
                    elif guess in self.guesses:
                        posa = self.guesses.index(guess)
                        if self.guesses[posa + 1] == "H":
                            x = xposguess
                            self.direction = 2
                        else:
                            if self.direction == 0:
                                rollfour = 3
                            else:
                                xypos = convert_position(self.firsthit)
                                self.direction = 1
                                counter += 1
                    else:
                        if self.direction == 0:
                            rollfour = 3
                        else:
                            xypos = convert_position(self.firsthit)
                            self.direction = 1
                            counter += 1
                if rollfour == 3:
                    yposguess = y + 1
                    guess = convert_coord(xypos[0], yposguess)
                    if guess and guess not in self.guesses:
                        ans = self.check_guess(guess, board)
                        if ans[1] == "H":
                            self.hits.append(guess)
                            self.direction = rollfour
                        elif ans[1] == "M":
                            self.direction = 4
                        return True
                    elif guess in self.guesses:
                        posa = self.guesses.index(guess)
                        if self.guesses[posa + 1] == "H":
                            y = yposguess
                            self.direction = 3
                        else:
                            if self.direction == 0:
                                rollfour = 4
                            else:
                                xypos = convert_position(self.firsthit)
                                self.direction = 4
                                counter += 1
                    else:
                        if self.direction == 0:
                            rollfour = 4
                        else:
                            xypos = convert_position(self.firsthit)
                            self.direction = 4
                            counter += 1
                if rollfour == 4:
                    yposguess = y - 1
                    guess = convert_coord(xypos[0], yposguess)
                    if guess and guess not in self.guesses:
                        ans = self.check_guess(guess, board)
                        if ans[1] == "H":
                            self.hits.append(guess)
                            self.direction = rollfour
                        elif ans[1] == "M":
                            self.direction = 3
                        return True
                    elif guess in self.guesses:
                        posa = self.guesses.index(guess)
                        if self.guesses[posa + 1] == "H":
                            y = yposguess
                            self.direction = 4
                        else:
                            if self.direction == 0:
                                rollfour = 1
                            else:
                                xypos = convert_position(self.firsthit)
                                self.direction = 3
                                counter += 1
                    else:
                        if self.direction == 0:
                            rollfour = 1
                        else:
                            xypos = convert_position(self.firsthit)
                            self.direction = 3
                            counter += 1
                if counter > 4:
                    rollfour = random.randint(1, 4)
        else:
            self.guess(board)
        return True

    def play(self, opponent):
        """
        will run the game
        :param opponent: of class board
        :return:
        """
        if self.difficulty == "master":
            self.mastermode(opponent)
        elif self.firsthit == "":
            self.guess(opponent)
        else:
            self.afterguess(self.guesses[-2], self.guesses[-1], opponent)
            q = self.check_sunk
            if q:
                self.remove_sunk_hits(q)
                if len(self.hits) > 0:
                    self.firsthit = self.hits[-1]
                else:
                    self.firsthit = ""
                self.direction = 0

    def place_ships(self):
        """
        will place the boats in a random spot and will flip for is it is a column or a row boat
        :return:
        """
        for key in self.boats:
            a = False
            while not a:
                row = random.randint(1, 10)
                column = random.randint(1, 10)
                startcoord = convert_coord(row, column)
                flip = random.randint(1, 2)
                if flip == 1:
                    if column <= key:
                        columnend = column + key - 1
                    else:
                        columnend = column - key - 1
                    endcoord = convert_coord(row, columnend)
                else:
                    if row <= key:
                        rowend = row + key - 1
                    else:
                        rowend = row - key - 1
                    endcoord = convert_coord(rowend, column)
                if startcoord and endcoord:
                    a = self.check_place_battleship(startcoord, endcoord, key)
                if key == 3 and len(self.boats[key][1]) != 3:
                    a = False
