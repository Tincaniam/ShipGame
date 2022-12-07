# Author: Matthew Tinnel
# GitHub username: Tincaniam
#
# This program allows two people to play the game Battleship.
# Each player has their own 10x10 grid they place their ships on. On their turn, they can fire a torpedo
# at a square on the enemy's grid. Player 'first' gets the first turn to fire a torpedo, after which players
# alternate firing torpedoes. A ship is sunk when all of its squares have been hit. When a player sinks their
# opponent's final ship, they win.

class ShipGamePlayer:
    """
    Represents a player object who is playing Battleship.
    All values are private.

    Has the following methods.

        [__init__] that creates an instance of a ShipGamePlayer.
        [get_player] that returns the name of the player.
        [get_board] that returns the player's "board" or graphical representation
            of their game.
        [get_navy] that returns the player's current fleet (inventory of placed ships(not yet destroyed)).
        [show_board] that calls self.get_board
    """

    def __init__(self, player):
        """
        Creates an instance of a ShipGamePlayer (player of the game Battleship).

        Takes as a parameter the player's name and sets it to the private data
        member self._player.

        Also intializes:

            self._board as a dictionary whose keys are the columns of the
            game board and whose values are the rows. This serves as a graphical representation
            for ShipGame.

            self._navy as an empty dictionary that will store the player's current fleet.
        """

        self._player = player

        self._board = {
            " " : ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
            "A" : [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "B": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "C": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "D": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "E": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "F": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "F": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "G": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "H": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "I": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            "J": [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        }

        self._navy = {}

    def get_player(self):
        """
        Takes no parameters.

        Returns the name of the player.
        """
        return self._player

    def get_board(self):
        """
        Takes no parameters.

        Returns the player's self._board.
        """
        return self._board

    def get_navy(self):
        """
        Takes no parameters.

        Returns the player's self._navy.
        """
        return self._navy

    def show_board(self, player):
        """
        Takes as a parameter the name of the player.

        Calls get_board() for the player, which will return that player's board.
        """
        player.get_board()

class ShipGame:
    """
    Represents the "game" itself of Battleship. Allows two people to play the game Battleship.

    Requires and uses the ShipGamePlayer class.

    All values are private.

    Has the following methods.

        [__init__] that creates an instance of a ShipGame object.
        [place_ship] that places the specified ship on the player's board, and in their navy.
        [get_current_state] returns the current state of the game: either 'FIRST_WON', 'SECOND_WON', or 'UNFINISHED'.]
        [fire_torpedo] that fires a "torpedo" at specified coordinates and destroys portions of ships
            or entire ships if all portions of a ship are destroyed.
        [get_num_ships_remaining] returns how many ships the specified player has left.
    """

    def __init__(self):
        """
        Creates an instance of a ShipGame object.

        All values are private.

        Also initializes:
            self._current_state as "UNFINISHED"
            self._first as a ShipGamePlayer object with the name "first".
            self._first as a ShipGamePlayer object with the name "second".
            self._whose_turn_is_it to "first".
        """
        self._current_state = "UNFINISHED"
        self._first = ShipGamePlayer("first")
        self._second = ShipGamePlayer("second")
        self._whose_turn_is_it = "first"

    def place_ship(self, player, length, coordinates, orientation):
        """
        Places the specified ship on the player's board, and in their navy.

        Takes as parameters:
            player - Which player is placing the ship ('first', or 'second').
            length - Length of the ship in spaces.
            coordinates - Where the "head" of the ship is located (closest to A1).
            orientation - Whether the ship is oriented by column or by row ('C', or 'R').

        Returns false if the ship does not fit entirely on that player's grid, or if would
        overlap with any previously placed ships on that player's grid, or if the length of
        the ship is less than 2.

        Uses:
            game_get_navy
            game_get_board
        """

        player_navy = self.game_get_navy(player)
        player_board = self.game_get_board(player)

        if length < 2:
            return False

        # Gets parsable data from "coordinates" and assigns it to "column", and "row"
        column = coordinates[0]
        # Catches edge case where ships are placed on 10th row.
        if len(coordinates) > 2:
            row = 10
        else:
            row = int(coordinates[1])
        # Decrements row to account for list indexing starting at 0.
        row -= 1

        # These will be used to place the "squares" the ship takes up for each
        # ship in the players navy.

        column_str = str(column)
        # increments it as this will be used for list indexing.
        row_str = str(row+1)
        coord_str = column_str + row_str

        # If the column entered is on the board in (" ", or range: "A" : "J")
        if column in player_board:
            # Gets the list for that row, which is a list with the column as the key.
            list_for_key = player_board[column]
            # Copies the list so the board isn't updated unless the entire ship is
            # placed.
            list_for_key_copy = list(list_for_key)
        else:
            return False

        # Preserve original length.
        length_copy = length

        # For placing ships with row ('R') orientation.
        if orientation == 'R':
            # Our base case, "length_copy" will be decremented.
            while length_copy > 0:
                # Checks ships from being placed off the board to the right or left, or
                # ships overwriting other ships.
                if row < 0 or row == len(list_for_key_copy) or list_for_key_copy[row] != " ":
                    return False
                else:
                    # Writes the current position of the ship to the board.
                    list_for_key_copy[row] = "o"
                    # Increments row, moving to the next row.
                    row += 1
                    # Decrements length_copy, decrementing our loop.
                    length_copy -= 1

                    # Updates these for new row values.
                    # Placing the square for the ship in the players
                    # navy each time the loop runs.
                    column_str = str(column)
                    row_str = str(row)
                    coord_str = column_str + row_str

                    # The players navy is a dictionary with the key being
                    # the coordinates and the values being a list containing each
                    # coordinate the ship takes up.

                    # If the ship is already in the navy.
                    if coordinates in player_navy:
                        # Add the current square to the ship in player_navy.
                        player_navy[coordinates].append(coord_str)
                    else:
                        # Else create a ship with current coordinates as the value
                        # in the player navy.
                        player_navy[coordinates] = [coord_str]

        # For placing ships with row ('C') orientation.
        elif orientation == 'C':

            # These are initialized out of the while loop will be utilized
            # inside.

            # Gets the ascii value for the char in "column"
            asc_column = ord(column)
            # Gets back the char from the ascii value.
            chr_column = chr(asc_column)

            # Finds the last (furthest from A) column the ship will take up.
            last_x = asc_column + length_copy -1    # Adjusts length for list indexing.
            last_x_chr = chr(last_x)                # Gets new chr value from asc value.
            # To be updated later in the loop.
            new_last_x_chr = last_x_chr

            # Our base case, "length_copy" will be decremented.
            while length_copy > 0:

                # Checks if the current column is in the player board, and the last character
                # the ship takes up is in player_board.
                if chr_column in player_board and new_last_x_chr in player_board:

                    # Updates these values for the new length.
                    last_x = asc_column + length_copy -1
                    chr_column = chr(last_x)
                    # Gets list for the current column.
                    list_for_key = player_board[chr_column]

                    # Checks to make sure we haven't gone off the board and that
                    # we aren't overwriting another ship.
                    if chr_column not in player_board or list_for_key[row] != " ":
                        return False
                    # Writes the ship to the board and updates values for looping.
                    else:
                        length_copy -= 1
                        new_last_x = asc_column + length_copy -1
                        new_last_x_chr = chr(new_last_x)
                        list_for_key[row] = "o"

                        row_str = str(row+1)
                        coord_str = chr_column + row_str

                        # Adds current coordinates to the navy as a square
                        # for this ship.
                        if coordinates in player_navy:
                            player_navy[coordinates].append(coord_str)
                        else:
                            player_navy[coordinates] = [coord_str]

                        # Exit case, catches edge cases of ships being placed in column 'J'.
                        if new_last_x_chr not in player_board:
                            return True
                        # Updates the list.
                        list_for_key = player_board[new_last_x_chr]

                else:
                    return False

            return True

        else:
            return False
        # Adds the copies list to the actual player's board.
        player_board[column] = list_for_key_copy
        return True

    def get_current_state(self):
        """
        Takes no paramaters.

        Returns self._current_state.
        """
        return self._current_state

    def fire_torpedo(self, player, coordinates):
        """
        Fires a "torpedo" at the passed coordinates. Updates ship state, whose turn
        it is, and if the move resulted in a win for either player.

        Returns False if it is not that player's turn, or if the game has already been won.

        Else returns True.

        Uses:
            whose_turn_is_it
            current_state
            game_get_navy
            game_get_board
        """

        # Checks if it is not that players turn, or if the game has already been won.
        if self._whose_turn_is_it != player or self._current_state != "UNFINISHED":
            return False
        else:
            # Gets the opposing player's navy and board, update whose turn it is.
            if player == "first":
                other_player_navy = self.game_get_navy("second")
                self._whose_turn_is_it = "second"
                other_players_board = self.game_get_board("second")
            else:
                other_player_navy = self.game_get_navy("first")
                self._whose_turn_is_it = "first"
                other_players_board = self.game_get_board("first")

            # Iterates through the lists of ships in the opposing players navy.
            for key, value_list in other_player_navy.items():
                # And for each square taken up by those ships.
                for each_value in value_list:
                    # If there is a ship square at the passed coordinates.
                    if each_value == coordinates:
                        # Remove that square from the ship and give some feedback to the user.
                        value_list.remove(coordinates)
                        print("Direct hit!")

            # Copies other_player_navy and iterates through that
            # to avoid changing size of dictionary during
            # iteration.
            for key, value_list in list(other_player_navy.items()):
                # If the ship has no squares left.
                if len(value_list) == 0:
                    # Remove the ship.
                    del other_player_navy[key]

            # If we destroyed the last ship.
            if len(other_player_navy) == 0:

                # Update current_state to declare the winner.
                if player == "first":
                    self._current_state = "FIRST_WON"
                else:
                    self._current_state = "SECOND_WON"

        # Updates the players graphical board.

        # Breaks out the coordinates as in place_ship.
        column = coordinates[0]
        if len(coordinates) > 2:
            row = 10
        else:
            row = int(coordinates[1])

        # Gets the list for the correct column.
        if column in other_players_board:
            list_for_key = other_players_board[column]
            # Accounts for list indexing.
            row -= 1

            # Updates the board to display the hit.
            if list_for_key[row] == "o":
                list_for_key[row] = "x"

        return True

    def get_num_ships_remaining(self, player):
        """
        Displays the number of ships remaining, or the number of ships in the players navy.

        Takes as a parameter the player's name ("first" or "second").

        Returns how many ships (keys) are in the players navy (dictionary).

        Uses game_get_navy.
        """
        navy = self.game_get_navy(player)
        return len(navy)


    def game_get_player(self, player):
        """
        Gets the player object from the player's text names "first" and "last".

        Takes as a parameter the player's name.

        Returns the resulting player object, else returns False.
        """
        if player == "first":
            return self._first
        if player == "second":
            return self._second
        else:
            return False

    def game_get_board(self, player):
        """
        Gets the board (dictionary) for the passed player.

        Takes as a parameter the player's name.

        Returns the player's board (dictionary).

        Uses:
            game_get_player
            get_board
        """

        player_obj = self.game_get_player(player)
        return player_obj.get_board()

    def game_get_navy(self, player):
        """
        Gets the navy (dictionary) for the passed player.

        Takes as a parameter the player's name.

        Returns the player's navy (dictionary).

        Uses:
            game_get_player
            get_navy
        """
        player_obj = self.game_get_player(player)
        return player_obj.get_navy()

    def game_show_board(self, player):
        """
        Prints the graphical game board to the screen for the passed player.

        Takes as a parameter the player's name.

        Uses:
            game_get_board
        """
        # Gets the board for the passed player, assigns it to "player_board".
        player_board = self.game_get_board(player)
        # Iterates through each key (column) in the dictionary player_board.
        for each_key in player_board:
            # Ensures each key is a string.
            string1 = str(each_key)
            # prints an extra space after the column headers for formatting.
            string1 += " "
            # Iterates for each value in each key.
            for each_value in player_board[each_key]:
                # Concats the column to each value in the row with a space in the middle.
                string1 += str(each_value + " ")
            # Prints the result to the display.
            print(string1)
            

if __name__ == "__main__":
