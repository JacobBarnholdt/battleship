from tkinter import *
import random

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

        #if self.gameboard.mode == 1:


        if self.matrix.is_my_turn():
            if (self.ship     != None) and (self.square["text"]   != "#"):
                self.square["text"]                                = "#"
                self.marked                                        = True
                self.matrix.mark_closeby_squares(self, self.ship)
                self.matrix.clear_info()
                self.matrix.is_all_ships_sunked()
            elif (self.square["text"] != "X") and (self.square["text"] != "#"):
                self.square["text"]                                = "X"
                self.matrix.change_player()
                self.matrix.computer_move()
            else:
                self.matrix.try_again()

            print("rutan %d %d" % (self.row, self.column))

        else:
            self.matrix.wrong_clicked()
        return

    #Dator spelar
    def try_click(self):
        finished = False
        if (self.ship     != None) and (self.square["text"] != "#"):
            self.square["text"]                              = "#"
            self.marked                                      = True
            self.matrix.mark_closeby_squares(self, self.ship)
            self.matrix.clear_info()
            self.matrix.is_all_ships_sunked()

        elif (self.square["text"] != "X") and (self.square["text"] != "#"):
            self.square["text"]                              = "X"
            finished                                         = True
            self.matrix.change_player()


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

    def show_hide_ships(self):
        if self.square["text"] == "O":
            self.square["text"] = "S"

        elif self.square["text"] == "#":
            self.square["text"] = "#"

        else:
            self.square["text"] = "O"
        return

#Matricen
class Matrix:
    def __init__(self, master, gameboard, matrix_number, cpu):
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

        #placerar ut skeppen i de olika rutorna på matricen
        for row in range(1, self.rows+1):
            squarerows = []

            for column in range(1, self.columns+1):
                square = Square(master, frame, row, column, self, self.gameboard)
                squarerows.append(square)
            self.squares.append(squarerows)


        self.ships.append(self.ship_making(1))
        self.ships.append(self.ship_making(2))
        self.ships.append(self.ship_making(3))
        self.ships.append(self.ship_making(4))
        self.ships.append(self.ship_making(5))
        #tests
        #self.ships.append(self.ship_making_without_random(5,2,2,False))
        #self.ships.append(self.ship_making_without_random(5,4,2,False))
        #self.ships.append(self.ship_making_without_random(5,8,6,False))
        #self.ships.append(self.ship_making_without_random(3,2,7,True))
        #self.ships.append(self.ship_making_without_random(5,7,2,True))

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
            return self.gameboard.win()
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

    #turodning
    def change_player(self):
        self.gameboard.change_player()
        return

    #felhantering fel spelare
    def wrong_clicked(self):
        return self.gameboard.wrong_clicked()

    #Felhantering klickat på markerad ruta
    def try_again(self):
        self.gameboard.try_again()
        return

    #Rensa notis ruta
    def clear_info(self):
        self.gameboard.clear_info()
        return

    #Datorn spelar
    def computer_move(self):
        if self.cpu:
            self.gameboard.computer_move()

    def show_hide_ships(self):
        for ship in self.ships:
            ship.show_hide_ship()
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
    def __init__(self, master, mode):
        self.master    = master
        frame          = Frame(master)
        frame.grid(row = 1, column = 2)
        self.frame     = frame
        self.btn_singleplayer  = Button(frame, text ="[SINGLEPLAYER]", command=self.singleplayer)
        self.btn_singleplayer.grid(row = 1, column  = 1)
        self.btn_multiplayer   = Button(frame, text ="[MULTIPLAYER]", command=self.multiplayer)
        self.btn_multiplayer.grid(row = 1, column   = 2)
        self.current_player = Label(master, text    = "", fg = "green")
        self.current_player.grid(row = 2, column    = 1)
        self.current   = 1
        self.info      = Label(master, text = "", fg = "red")
        self.info.grid(row = 2, column = 2)
        self.lbl_win   = Label(master, text = "")
        self.lbl_win.grid(row = 2, column = 5)
        self.btn_show_player2_ships = Button(frame, text ="[Show/Hide Player2 Ships]", command = self.show_hide_ship_player1)
        self.btn_show_player2_ships.grid(row = 2, column = 8)
        self.matrix1   = None
        self.btn_show_player1_ships = Button(frame, text ="[Show/Hide Player1 Ships]", command = self.show_hide_ship_player2)
        self.btn_show_player1_ships.grid(row = 2, column = 9)
        self.matrix2   = None
        self.btn_5_ship = Button(frame, text = "Creat Carrier(5)", command = self.create_5_ship)
        self.btn_5_ship.grid(row = 2, column = 1)
        self.btn_4_ship = Button(frame, text = "Creat Battleship(4)", command = self.create_4_ship)
        self.btn_4_ship.grid(row = 3, column = 1)
        self.btn_3_ship = Button(frame, text = "Creat Submarine(3)", command = self.create_3_ship)
        self.btn_3_ship.grid(row = 4, column = 1)
        self.btn_2_ship = Button(frame, text = "Creat Cruiser(2)", command   = self.create_2_ship)
        self.btn_2_ship.grid(row = 5, column = 1)
        self.btn_1_ship = Button(frame, text = "Creat Destroyer(1)", command = self.create_1_ship)
        self.btn_1_ship.grid(row = 6, column = 1)
        self.btn_start_game = Button(frame, text ="Start Game", command      = self.start_game())
        self.btn_start_game.grid(row = 5, column = 5)
        self.player_one_name = None
        self.player_two_name = None
        self.mode = None
        return

    def current_turn(self):
        if self.current == 1:
            self.current_player["text"] = "Player Ones Turn"
        else:
            self.current_player["text"] = "Player Twos Turn"
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

    def wrong_clicked(self):
        self.info["text"] = "Shame Shame I Know Your Name"
        return

    def try_again(self):
        self.info["text"] = "Try again!"
        return

    def clear_info(self):
        self.info["text"] = ""
        return

    def win(self):
        self.lbl_win["text"] = "Congratulations You Won"
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
        pass

    def create_4_ship(self):
        pass

    def create_3_ship(self):
        pass

    def create_2_ship(self):
        pass

    def create_1_ship(self):
        pass

    def start_game(self):
        self.mode = 2
        return

    def singleplayer(self):
        dialog = MyDialog(self.frame, "Ange ditt namn", "Namn")
        self.frame.wait_window(dialog.top)
        self.player_one_name = dialog.value
        self.player_two_name = "CPU"
        self.btn_show_player1_ships["text"] = "Show/Hide " + str(dialog.value)+"s" + " Ships"
        self.btn_show_player2_ships["text"] = "Show/Hide CPUs Ships"
        self.matrix2 = Matrix(self.master, self, 2, cpu = True)
        self.matrix1 = Matrix(self.master, self, 1, cpu = True)
        self.current_turn()
        self.mode = 1
        return

    def multiplayer(self):
        dialog = MyDialog(self.frame, "Ange första spelarns namn", "Namn")
        self.frame.wait_window(dialog.top)
        self.player_one_name = dialog.value
        dialog2 = MyDialog(self.frame, "Ange andra spelarns namn", "Namn")
        self.frame.wait_window(dialog2.top)
        self.player_two_name = dialog2.value
        self.btn_show_player1_ships["text"] = "Show/Hide " + str(dialog.value)+"s" + " Ships"
        self.btn_show_player2_ships["text"] = "Show/Hide " + str(dialog2.value)+"s" + " Ships"
        self.matrix1 = Matrix(self.master, self, 1, cpu = False)
        self.matrix2 = Matrix(self.master, self, 2, cpu = False)
        self.current_turn()
        self.mode = 1
        return




root = Tk()
root.title("Battleship")
gameboar = Gameboard(root, 1)
root.mainloop()
