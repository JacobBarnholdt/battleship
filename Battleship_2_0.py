from tkinter import *
import random

from Highscore import Highscores


#Pop-up ruta när man skriver namn
class MyDialog:
    def __init__(self, parent, prompt, title):
        top = self.top = Toplevel(parent)
        top.title(title)
        Label(top, text=prompt).pack()
        self.e = Entry(top)
        self.e.pack(padx=5)
        b = Button(top, text="OK", command=self.ok)
        b.pack(pady=5)
        self.value = None

    def ok(self):
        print("value is " + self.e.get())
        self.value = self.e.get()
        self.top.destroy()

#Klass skepp
class Ship:
    def __init__(self, row, column, vertical, extent, squares, rows, columns):
        self.row           = row
        self.column        = column
        self.vertical      = vertical
        self.extent        = extent
        self.squares       = []
        self.amountRows    = rows
        self.amountColumns = columns

        if vertical:
            for row in range(self.row, self.row + extent):
                self.squares.append(squares[row - 1][column - 1])
                squares[row - 1][column - 1].add_ship(self)

        else:
            for column in range(self.column, self.column + extent):
                self.squares.append(squares[row - 1][column - 1])
                squares[row - 1][column - 1].add_ship(self)
        return

    #utsträckning
    def get_extent(self):
        return self.extent

    def get_vertical(self):
        return self.vertical

    def set_vertical(self, vertical):
        self.vertical = vertical
        return

    #sista ruta i en rad
    def get_endsquare_row(self):
        if self.vertical:
            if (self.row != 1):
                return self.row - 1
            else:
                return self.row
        else:
            return self.row

    #sista ruta i en kolumn
    def get_endsquare_column(self):
        if self.vertical:
            return self.column
        else:
            if (self.column != 1):
                return self.column - 1
            else:
                return self.column

    #sista ruta i rad
    def get_other_endsquare_row(self):
        if self.vertical:
            if (self.row -1 + self.extent != self.amountRows):
                return self.row + self.extent
            else:
                return self.row
        else:
            return self.row

    #sista ruta i kolumn
    def get_other_endsquare_column(self):
        if self.vertical:
            return self.column
        else:
            if self.column -1 + self.extent != self.amountColumns:
                return self.column + self.extent
            else:
                return self.column

    #sjunket skepp
    def is_sink(self):
        sink             = True
        for square in self.squares:
            sink         = square.is_marked() and sink
        return sink

    #tjuvkika
    def show_hide_ship(self):
        for square in self.squares:
            square.show_hide_ships()
        return

    def show_ship(self):
        for square in self.squares:
            square.show_ship()
        return

    def hide_ship(self):
        for square in self.squares:
            square.hide_ship()
        return

#Ruta
class Square:
    def __init__(self, master, frame, row, column, matrix, gameboard):
        self.square      = Button(frame, text="O", width = 2, command=self.marked)
        self.marked      = False
        self.frame       = frame
        self.row         = row
        self.column      = column
        self.square.grid(row = row - 1, column = column - 1)
        self.ship        = None
        self.matrix      = matrix
        self.gameboard   = gameboard

    #hitta rad
    def get_row(self):
        return self.row

    #hitta kolumn
    def get_column(self):
        return self.column

    #Ruta markerad
    def is_marked(self):
        return self.marked

    #Ruta innehåller sepp
    def has_ship(self):
        return self.ship != None

    # Metod för att hantera musklick på en spelruta
    def marked(self):

        self.gameboard.clear_info()
        if self.gameboard.mode == 30:  # playing
            if self.matrix.is_my_turn():
                if (self.ship     != None) and (self.square["text"]   != "#"):
                    self.square["text"]                                = "#"
                    self.marked                                        = True
                    self.matrix.nr_of_clicks = self.matrix.nr_of_clicks + 1
                    self.matrix.mark_closeby_squares(self, self.ship)
                    self.gameboard.clear_info()
                    self.matrix.is_all_ships_sunked()
                elif (self.square["text"] != "X") and (self.square["text"] != "#"):
                    self.square["text"]                                = "X"
                    self.matrix.nr_of_clicks = self.matrix.nr_of_clicks + 1
                    self.gameboard.change_player()
                    self.matrix.computer_move()
                else:
                    self.gameboard.set_info("Try Again")
                print("rutan %d %d" % (self.row, self.column))
            else:
                self.gameboard.set_info("Shame Shame I Know Your Name")

        elif self.gameboard.mode == 20: #  placing ships
            if self.gameboard.singleplayer_mode:
                self.gameboard.current = 2
                if self.matrix.is_my_turn():
                    if (self.matrix.nr_of_5_ships > 0) and (self.gameboard.current_ship_extent == 5):
                        self.gameboard.set_info("Can't Place more than one Carrier")
                    else:
                        self.matrix.try_place_ship(self.row, self.column)
                else:
                    self.gameboard.set_info("Can't Place Ship There")
            else:
                if self.gameboard.matrix2.nr_of_ships < 5:
                    self.gameboard.set_info("Player " + self.gameboard.player_two_name + "s turn")
                    self.gameboard.current = 1
                    if self.matrix.is_my_turn():
                        self.matrix.try_place_ship(self.row, self.column)
                        if self.matrix.nr_of_ships == 5:
                            self.gameboard.set_info("Player " + self.gameboard.player_one_name + "s turn")
                    else:
                        self.gameboard.set_info("Can't Place Ship There")
                elif self.gameboard.matrix1.nr_of_ships < 5:
                    self.gameboard.set_info("Player " + self.gameboard.player_one_name + "s turn")
                    self.gameboard.current = 2
                    if self.matrix.is_my_turn():
                        self.matrix.try_place_ship(self.row, self.column)
                        if self.matrix.nr_of_ships == 5:
                            self.gameboard.set_info("You are now ready to start game")
                    else:
                        self.gameboard.set_info("You Can't Place a Ship There")
                else:
                    self.gameboard.set_info("You are now ready to start game")



        return

    #Dator spelar
    def try_click(self):
        finished = False
        if (self.ship     != None) and (self.square["text"] != "#"):
            self.square["text"]                              = "#"
            self.marked                                      = True
            self.matrix.nr_of_clicks = self.matrix.nr_of_clicks + 1
            self.matrix.mark_closeby_squares(self, self.ship)
            self.gameboard.clear_info()
            self.matrix.is_all_ships_sunked()

        elif (self.square["text"] != "X") and (self.square["text"] != "#"):
            self.square["text"]                              = "X"
            self.matrix.nr_of_clicks = self.matrix.nr_of_clicks + 1
            finished                                         = True
            self.gameboard.change_player()


        print("rutan %d %d" % (self.row, self.column))
        return finished

    #Markerar ruta
    def set_marked(self):
        if self.ship == None:
            self.square["text"] = "X"
        else:
            self.square["text"] = "#"
        self.marked             = True
        return

    #Lägger till skepp på ruta
    def add_ship(self, ship):
        self.ship           = ship
        self.square["text"] = "O"
        return

    def remove_ship(self):
        self.ship = None

    def show_hide_ships(self):
        if self.square["text"] == "O":
            self.square["text"] = "S"

        elif self.square["text"] == "#":
            self.square["text"] = "#"

        else:
            self.square["text"] = "O"
        return

    def show_ship(self):
        self.square["text"] = "S"
        
    def hide_ship(self):
        self.square["text"] = "O"

#Matricen
class Matrix:
    def __init__(self, master, gameboard, matrix_number, cpu, name):
        frame          = Frame(master, bd = 5, bg = "blue")
        frame.grid(row = 3, column = matrix_number)
        self.gameboard = gameboard
        self.matrix_number = matrix_number
        self.cpu = cpu
        self.frame     = frame
        self.rows      = 10
        self.columns   = 10
        self.squares   = []
        self.ships     = []
        self.nr_of_1_ships = 0
        self.nr_of_2_ships = 0
        self.nr_of_3_ships = 0
        self.nr_of_4_ships = 0
        self.nr_of_5_ships = 0
        self.nr_of_ships = 0
        self.name = name
        self.nr_of_clicks = 0

        if self.matrix_number == 1:
            column = 1
        else:
            column = 2

        self.lbl_number_of_destroyers = Label(self.gameboard.master, text = "Player: "+ self.name)
        self.lbl_number_of_destroyers.grid(row = 6, column = column)
        self.lbl_number_of_destroyers = Label(self.gameboard.master, text = "Amount of destroyers: "+str(self.nr_of_1_ships))
        self.lbl_number_of_destroyers.grid(row = 7, column = column)
        self.lbl_number_of_cruiser = Label(self.gameboard.master, text = "Amount of Cruisers: "+str(self.nr_of_2_ships))
        self.lbl_number_of_cruiser.grid(row = 8, column= column)
        self.lbl_number_of_submarines = Label(self.gameboard.master, text = "Amount of Submarines: "+str(self.nr_of_3_ships))
        self.lbl_number_of_submarines.grid(row = 9, column = column)
        self.lbl_number_of_battleship = Label(self.gameboard.master, text = "Amount of Battleships: "+str(self.nr_of_4_ships))
        self.lbl_number_of_battleship.grid(row = 10, column = column)
        self.lbl_number_of_carriers = Label(self.gameboard.master, text = "Amount of Carriers: "+str(self.nr_of_5_ships))
        self.lbl_number_of_carriers.grid(row = 11, column = column)


        #Skapar spelplanen
        for row in range(1, self.rows+1):
            squarerows = []

            for column in range(1, self.columns+1):
                square = Square(master, frame, row, column, self, self.gameboard)
                squarerows.append(square)
            self.squares.append(squarerows)

        #tests
        #self.ships.append(self.ship_making_without_random(5,2,2,False))
        #self.ships.append(self.ship_making_without_random(5,4,2,False))
        #self.ships.append(self.ship_making_without_random(5,8,6,False))
        #self.ships.append(self.ship_making_without_random(3,2,7,True))
        #self.ships.append(self.ship_making_without_random(5,7,2,True))

        return

    def calculate_score(self):
        ship_square_count = 0
        for ship in self.ships:
            ship_square_count = ship.extent + ship_square_count
        score = self.nr_of_clicks - ship_square_count
        return score

    def auto_place_ships(self, other_matrix):
        for ship1s in range(0,other_matrix.nr_of_1_ships):
            self.ships.append(self.ship_making(1))
            self.nr_of_1_ships = self.nr_of_1_ships + 1
            self.nr_of_ships   = self.nr_of_ships + 1
        for ship2s in range(0,other_matrix.nr_of_2_ships):
            self.ships.append(self.ship_making(2))
            self.nr_of_2_ships = self.nr_of_2_ships + 1
            self.nr_of_ships   = self.nr_of_ships + 1
        for ship3s in range(0,other_matrix.nr_of_3_ships):
            self.ships.append(self.ship_making(3))
            self.nr_of_3_ships = self.nr_of_3_ships + 1
            self.nr_of_ships   = self.nr_of_ships + 1
        for ship4s in range(0,other_matrix.nr_of_4_ships):
            self.ships.append(self.ship_making(4))
            self.nr_of_4_ships = self.nr_of_4_ships + 1
            self.nr_of_ships   = self.nr_of_ships + 1
        for ship5s in range(0,other_matrix.nr_of_5_ships):
            self.ships.append(self.ship_making(5))
            self.nr_of_5_ships = self.nr_of_5_ships + 1
            self.nr_of_ships   = self.nr_of_ships + 1
        return

    #Konstruerar skepp
    def ship_making(self, extent):
        found_place_for_ship = False
        while not found_place_for_ship:
            x = self.gameboard.get_random_coordinate(10)
            y = self.gameboard.get_random_coordinate(10-extent)
            vertical = self.gameboard.get_random_coordinate(2) == 1
            found_place_for_ship = self.possible_to_place_ship(x, y, vertical, extent)

        ship = Ship(x, y, vertical, extent, self.squares, self.rows, self.columns)
        return ship

    #Konstruerar skepp
    def ship_making_without_random(self, extent,x,y,vertical):
        found_place_for_ship = False
        while not found_place_for_ship:
            found_place_for_ship = self.possible_to_place_ship(x, y, vertical, extent)

        ship = Ship(x, y, vertical, extent, self.squares, self.rows, self.columns)
        return ship

    def try_place_ship(self, row, column):
        vertical = self.gameboard.current_ship_vertical
        extent   = self.gameboard.current_ship_extent
        if self.nr_of_ships < 5:
            if self.possible_to_place_ship(row, column, vertical, extent):
                ship = Ship(row, column, vertical, extent, self.squares, self.rows, self.columns)
                ship.show_ship()
                self.ships.append(ship)
                self.nr_of_ships = self.nr_of_ships + 1
                if extent == 1:
                    self.nr_of_1_ships = self.nr_of_1_ships + 1
                elif extent == 2:
                    self.nr_of_2_ships = self.nr_of_2_ships + 1
                elif extent == 3:
                    self.nr_of_3_ships = self.nr_of_3_ships + 1
                elif extent == 4:
                    self.nr_of_4_ships = self.nr_of_4_ships + 1
                elif extent == 5:
                    self.nr_of_5_ships = self.nr_of_5_ships + 1
                self.update_amount_labels()
            else:
                self.gameboard.set_info("You Can't Place A Ship There")
        else:
            self.gameboard.set_info("You Have Placed Maximum Amount Of Ships")

    def update_amount_labels(self):
        self.lbl_number_of_destroyers["text"] = "Amount of Destroyers: "+str(self.nr_of_1_ships)
        self.lbl_number_of_cruiser["text"] = "Amount of Cruisers: "+str(self.nr_of_2_ships)
        self.lbl_number_of_submarines["text"] = "Amount of Submarines: "+str(self.nr_of_3_ships)
        self.lbl_number_of_battleship["text"] = "Amount of Battlehips: "+str(self.nr_of_4_ships)
        self.lbl_number_of_carriers["text"] = "Amount of Carriers: " +str(self.nr_of_5_ships)
        return

    #krav för placering av skepp
    def possible_to_place_ship(self, in_x, in_y, vertical, extent):
        result = True
        x = in_x - 1
        y = in_y - 1
        if x < 0:
            result = False
        if y < 0:
            result = False
        #print("Trying x = "+str(x)+" y = "+str(y)+" extent = "+str(extent)+" vertical="+str(vertical))
        if not vertical:
            z = x
            x = y
            y = z
        if x > 0:
            start = (x-1)
        else:
            start = x

        if (x + extent) < 10:
            end = (x + extent)
        elif (x + extent - 1) < 10:
            end = (x + extent -1)
        else:
            result = False

        if result:
            if vertical:
                for px in range((start), (end+1)):
                    #print("px = %d y = %d" % (px, y))
                    if y > 0:
                        result = result and (self.squares[px][(y-1)].has_ship() != True)
                    result = result and (self.squares[px][(y)].has_ship() != True)
                    if y < 9:
                        result = result and (self.squares[px][(y+1)].has_ship() != True)
            else:
                for px in range((start), (end+1)):
                    #print("px = %d y = %d" % (px, y))
                    if y > 0:
                        result = result and (self.squares[(y-1)][px].has_ship() != True)
                    result = result and (self.squares[y][px].has_ship() != True)
                    if y < 9:
                        result = result and (self.squares[(y+1)][px].has_ship() != True)

        if result:
            print("success")
        else:
            print("failed")
        return result

    #Är spelet vunnet funktion
    def is_all_ships_sunked(self):
        win = True
        for ships in range(0, len(self.ships)):
            ship = self.ships[ships]
            win = ship.is_sink() and win
        if win:
            return self.gameboard.win(self)
        return

    #Krav vid träff
    def mark_closeby_squares(self, square, ship):
        if ship.is_sink():
            self.hit_marks(square, ship)
        self.mark_diagonals(square, ship)
        return

    #turordning
    def is_my_turn(self):
        return self.matrix_number == self.gameboard.whos_turn_is_it()

    #Datorn spelar
    def try_move(self, x, y):
        square = self.squares[x-1][y-1]
        return square.try_click()


    #Datorn spelar
    def computer_move(self):
        if self.cpu:
            self.gameboard.computer_move()

    def show_hide_ships(self):
        for ship in self.ships:
            ship.show_hide_ship()
        return

    def hide_ships(self):
        for ship in self.ships:
            ship.hide_ship()
        return

    def delete_ships(self):
        self.hide_ships()
        self.ships = []
        self.nr_of_ships = 0
        self.nr_of_1_ships = 0
        self.nr_of_2_ships = 0
        self.nr_of_3_ships = 0
        self.nr_of_4_ships = 0
        self.nr_of_5_ships = 0
        for squarerow in self.squares:
            for square in squarerow:
                square.remove_ship()
        self.update_amount_labels()
        return

    #Markera diagonaler
    def mark_diagonals(self, square, ship):
        row                = square.get_row()
        column             = square.get_column()
        list_row           = square.get_row() - 1
        list_column        = square.get_column() - 1

        print("row=%d column = %d list_row = %d list_column = %d self.coumns = %d" % (row, column, list_row, list_column, self.columns))
        if (row > 1) and (row < self.rows) and (column > 1) and (column < self.columns):
            northwest      = self.squares[list_row - 1][list_column - 1]
            northeast      = self.squares[list_row - 1][list_column + 1]
            southwest      = self.squares[list_row + 1][list_column - 1]
            southeast      = self.squares[list_row + 1][list_column + 1]
            northwest.set_marked()
            northeast.set_marked()
            southwest.set_marked()
            southeast.set_marked()

        elif row == 1 and column == 1:
            southeast      = self.squares[list_row + 1][list_column + 1]
            southeast.set_marked()

        elif row ==1 and column == self.columns:
            southwest     = self.squares[list_row + 1][list_column - 1]
            southwest.set_marked()

        elif row == self.rows and column == 1:
            northeast     = self.squares[list_row - 1][list_column + 1]
            northeast.set_marked()

        elif row == self.rows and column == self.columns:
            northwest     = self.squares[list_row - 1][list_column - 1]
            northwest.set_marked()

        elif row == 1:
            southwest     = self.squares[list_row + 1][list_column - 1]
            southeast     = self.squares[list_row + 1][list_column + 1]
            southwest.set_marked()
            southeast.set_marked()

        elif row == self.rows:
            northwest     = self.squares[list_row - 1][list_column - 1]
            northeast     = self.squares[list_row - 1][list_column + 1]
            northwest.set_marked()
            northeast.set_marked()

        elif column == 1:
            northeast     = self.squares[list_row - 1][list_column + 1]
            southeast     = self.squares[list_row + 1][list_column + 1]
            northeast.set_marked()
            southeast.set_marked()

        elif column == self.columns:
            northwest     = self.squares[list_row - 1][list_column - 1]
            southwest     = self.squares[list_row + 1][list_column - 1]
            northwest.set_marked()
            southwest.set_marked()

    #Markering av sjunket skepp
    def hit_marks(self, square, ship):
        endsquare        = self.squares[ship.get_endsquare_row()-1][ship.get_endsquare_column()-1]
        other_endsquare  = self.squares[ship.get_other_endsquare_row()-1][ship.get_other_endsquare_column()-1]
        endsquare.set_marked()
        other_endsquare.set_marked()
        if ship.get_extent() == 1:
            ship.set_vertical(not ship.get_vertical())
            endsquare        = self.squares[ship.get_endsquare_row()-1][ship.get_endsquare_column()-1]
            other_endsquare  = self.squares[ship.get_other_endsquare_row()-1][ship.get_other_endsquare_column()-1]
            endsquare.set_marked()
            other_endsquare.set_marked()
        return


class Gameboard:
    def __init__(self, master):
        self.highscores = Highscores()
        self.master    = master
        frame          = Frame(master)
        frame.grid(row = 1, column = 2)
        self.frame     = frame
        self.btn_singleplayer  = Button(frame, text ="[SINGLEPLAYER]", command=self.singleplayer)
        self.btn_singleplayer.grid(row = 1, column  = 1)
        self.btn_multiplayer   = Button(frame, text ="[MULTIPLAYER]", command=self.multiplayer)
        self.btn_multiplayer.grid(row = 1, column   = 2)
        self.btn_exit_game     = Button(frame, text ="[Exit Game]", command=self.quit)
        self.btn_exit_game.grid(row = 1, column = 10)
        highscoretext = self.highscores.get_scores()
        self.lbl_high_score = Label(master,text = highscoretext)
        self.lbl_high_score.grid(row = 1, column = 11)
        self.current_player = Label(master, text    = "", fg = "green")
        self.current_player.grid(row = 2, column    = 1)
        self.info      = Label(master, text = "", fg = "red")
        self.info.grid(row = 2, column = 2)
        self.matrix1   = None
        self.matrix2   = None
        self.player_one_name = None
        self.player_two_name = None
        self.mode = 10  #  val av spelmode
        self.current_ship_vertical = False
        self.current_ship_extent = 1
        return

    def current_turn(self):
        if self.current == 1:
            self.current_player["text"] = "Player " + self.player_one_name + "s Turn"
        else:
            self.current_player["text"] = "Player " + self.player_two_name + "s Turn"
        return

    def whos_turn_is_it(self):
        return self.current

    def change_player(self):
        if self.current == 1:
            self.current = 2
        else:
            self.current = 1
        self.current_turn()
        self.clear_info()
        return

    def quit(self):
        root.destroy()

    def set_info(self,text):
        self.info["text"] = text

    def clear_info(self):
        self.info["text"] = ""
        return

    def win(self,matrix):
        if matrix == self.matrix2:
            winning_matrix = self.matrix1
            losing_matrix  = self.matrix2
        else:
            winning_matrix = self.matrix2
            losing_matrix  = self.matrix1
        score = losing_matrix.calculate_score()
        self.info["text"] = "Congratulations " + winning_matrix.name + " Won with score " + str(score)
        self.highscores.add_score(winning_matrix.name,score)
        highscoretext = self.highscores.get_scores()
        self.lbl_high_score["text"] = highscoretext
        self.mode = 40
        return

    def show_hide_ship_player1(self):
         self.matrix1.show_hide_ships()
         return

    def show_hide_ship_player2(self):
        self.matrix2.show_hide_ships()
        return

    def computer_move(self):
        valid_move = False
        while not valid_move:
            x = self.get_random_coordinate(10)
            y = self.get_random_coordinate(10)
            valid_move = self.matrix2.try_move(x,y)
        return

    def get_random_coordinate(self, x):
        return random.randint(1, x)

    def create_5_ship(self):
        self.current_ship_extent = 5
        self.set_ship_button_highlight()
        return

    def create_4_ship(self):
        self.current_ship_extent = 4
        self.set_ship_button_highlight()
        return

    def create_3_ship(self):
        self.current_ship_extent = 3
        self.set_ship_button_highlight()
        return

    def create_2_ship(self):
        self.current_ship_extent = 2
        self.set_ship_button_highlight()
        return

    def create_1_ship(self):
        self.current_ship_extent = 1
        self.set_ship_button_highlight()
        return

    def create_vertical_on_off(self):
        if self.current_ship_vertical:
            self.current_ship_vertical = False
            self.btn_vertical_on_off["fg"] = "black"
        else:
            self.current_ship_vertical = True
            self.btn_vertical_on_off["fg"] = "red"
        return

    def set_ship_button_highlight(self):
        self.btn_1_ship["state"] = NORMAL
        self.btn_2_ship["state"] = NORMAL
        self.btn_3_ship["fg"] = "black"
        self.btn_4_ship["fg"] = "black"
        self.btn_5_ship["fg"] = "black"
        if self.current_ship_extent == 1:
            self.btn_1_ship.flash()
        elif self.current_ship_extent == 2:
            self.btn_2_ship.flash()
        elif self.current_ship_extent == 3:
            self.btn_3_ship["fg"] = "red"
        elif self.current_ship_extent == 4:
            self.btn_4_ship["fg"] = "red"
        elif self.current_ship_extent == 5:
            self.btn_5_ship["fg"] = "red"
        return

    def start_game(self):

        if self.singleplayer_mode:
            self.matrix1.auto_place_ships(self.matrix2)
            self.matrix2.hide_ships()

        else:
            self.matrix1.hide_ships()
            self.matrix2.hide_ships()

        if self.can_we_start():
            self.btn_1_ship.grid_forget()
            self.btn_2_ship.grid_forget()
            self.btn_3_ship.grid_forget()
            self.btn_4_ship.grid_forget()
            self.btn_5_ship.grid_forget()
            self.btn_vertical_on_off.grid_forget()
            self.btn_start_game.grid_forget()
            self.btn_reset_ships.grid_forget()
            # destroy other shipplacer mode = 20 buttons
            self.mode = 30
            self.current   = 1
            self.set_info("")
        else:
            self.info["text"] = "Not equal amount of ships between players"

        return

    def can_we_start(self):
        result = True
        if (self.matrix1.nr_of_ships == 0):
            result = False
        if self.matrix1.nr_of_1_ships != self.matrix2.nr_of_1_ships:
            result = False
        elif self.matrix1.nr_of_2_ships != self.matrix2.nr_of_2_ships:
            result = False
        elif self.matrix1.nr_of_3_ships != self.matrix2.nr_of_3_ships:
            result = False
        elif self.matrix1.nr_of_4_ships != self.matrix2.nr_of_4_ships:
            result = False
        elif self.matrix1.nr_of_5_ships != self.matrix2.nr_of_5_ships:
            result = False
        return result

    def singleplayer(self):
        self.singleplayer_mode = True
        dialog = MyDialog(self.frame, "Ange ditt namn", "Namn")
        self.frame.wait_window(dialog.top)
        self.player_one_name = "CPU"
        self.player_two_name = str(dialog.value)
        self.matrix2 = Matrix(self.master, self, 2, False, self.player_two_name)
        self.matrix1 = Matrix(self.master, self, 1, True, self.player_one_name)
        self.start_placing_ships()
        return

    def multiplayer(self):
        self.singleplayer_mode = False
        dialog = MyDialog(self.frame, "Ange första spelarns namn", "Namn")
        self.frame.wait_window(dialog.top)
        self.player_one_name = dialog.value
        dialog2 = MyDialog(self.frame, "Ange andra spelarns namn", "Namn")
        self.frame.wait_window(dialog2.top)
        self.player_two_name = dialog2.value
        self.matrix2 = Matrix(self.master, self, 1, False, self.player_two_name)
        self.matrix1 = Matrix(self.master, self, 2, False, self.player_one_name)
        self.start_placing_ships()
        return


    def reset_ships(self):
        self.matrix1.delete_ships()
        self.matrix2.delete_ships()
        self.current = 1

        return

    def start_placing_ships(self):
        self.btn_reset_ships = Button(self.frame, text = "[Reset Ships]", command = self.reset_ships)
        self.btn_reset_ships.grid(row = 10, column = 10)
        self.btn_5_ship = Button(self.frame, text = "Creat Carrier(5)", command = self.create_5_ship)
        self.btn_5_ship.grid(row = 2, column = 1)
        self.btn_4_ship = Button(self.frame, text = "Creat Battleship(4)", command = self.create_4_ship)
        self.btn_4_ship.grid(row = 3, column = 1)
        self.btn_3_ship = Button(self.frame, text = "Creat Submarine(3)", command = self.create_3_ship)
        self.btn_3_ship.grid(row = 4, column = 1)
        self.btn_2_ship = Button(self.frame, text = "Creat Cruiser(2)", command   = self.create_2_ship)
        self.btn_2_ship.grid(row = 5, column = 1)
        self.btn_1_ship = Button(self.frame, text = "Creat Destroyer(1)", command = self.create_1_ship)
        self.btn_1_ship.grid(row = 6, column = 1)
        self.btn_vertical_on_off = Button(self.frame, text = "Vertical On", command = self.create_vertical_on_off)
        self.btn_vertical_on_off.grid(row = 7, column = 1)
        self.btn_start_game = Button(self.frame, text ="Start Game", command = self.start_game)
        self.btn_start_game.grid(row = 5, column = 5)
        self.btn_singleplayer.grid_forget()
        self.btn_multiplayer.grid_forget()
        self.matrix1.show_hide_ships()
        self.matrix2.show_hide_ships()


        self.btn_show_player2_ships = Button(self.frame, text ="[Show/Hide Player2 Ships]", command = self.show_hide_ship_player1)
        self.btn_show_player2_ships.grid(row = 2, column = 8)
        self.btn_show_player1_ships = Button(self.frame, text ="[Show/Hide Player1 Ships]", command = self.show_hide_ship_player2)
        self.btn_show_player1_ships.grid(row = 2, column = 9)
        self.btn_show_player2_ships["text"] = "Show/Hide " + self.player_one_name +"s" + " Ships"
        self.btn_show_player1_ships["text"] = "Show/Hide " + self.player_two_name +"s Ships"
        self.set_info("Player "+ self.player_two_name +"s turn to place ships")
        self.mode = 20
        return


root = Tk()
root.title("Battleship")
gameboard = Gameboard(root)
root.mainloop()
