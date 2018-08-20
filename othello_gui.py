#othello_gui.py
#Alexandra Movsesyan
#42206297

import tkinter
import collections
import othello_game_logic
from othello_game_logic import Gamestate

BLACK = 'black'
WHITE = 'white'

DEFAULT_FONT = ('Arial', 14)
Disk = collections.namedtuple('Disk', ['color', 'board_index'])

class Othello:
    def __init__(self):
        '''
        Initializes the Othello game and greates a Tkinter window with a canvas containing a header and footer
        Sets attributes of Othello
        '''
        self._root_window = tkinter.Tk()

        self._start_button = tkinter.Button(
            master = self._root_window, text = 'Start Game', font = DEFAULT_FONT,
            command = self._set_up_game)

        self._start_button.grid(row= 2, column = 0, padx = 10, pady = 10,
            sticky = tkinter.S)

        self._canvas = tkinter.Canvas(
            master = self._root_window,
            width = 400, height = 400, background = '#95b7ed', highlightthickness=0)

        self._canvas.grid(
            row = 1, column = 0, padx = 0, pady =0,
            sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)
        
        self._title_label = tkinter.Label(
            master = self._root_window, text = 'OTHELLO\n(Full)', background = '#95b7ed',
            font = ('Arial',56))
        

        self._title_label.grid(
            row = 1, column = 0, padx =0, pady=0,
            sticky = tkinter.N + tkinter.S + tkinter.W + tkinter.E)

        self._header = tkinter.Label(
            master = self._root_window, text = '', background = 'white',
            font = ('Arial', 25))

        self._header.grid(
            row = 0, column = 0, padx = 0, pady = 0,
            sticky = tkinter.S+tkinter.N+tkinter.W+ tkinter.E)
        
        self._root_window.rowconfigure(0, weight = 1)
        self._root_window.rowconfigure(1, weight = 3)
        self._root_window.rowconfigure(2, weight = 1)
        self._root_window.columnconfigure(0, weight = 1)

        self._gamestate = None

        self._disks = []

        self._winner = None

        self._initial_disk_done = False

        self._row_index=None
        self._column_index=None

        self._row_col_input = False
        self._first_player_input = False
        self._how_won_input = False


        
    def run_game(self)-> None:
        '''
        Runs event based Othello Game
        '''
        self._root_window.mainloop()

    def _get_input(self)-> None:
        '''
        Opens a dialog box to ask user for number of rows, columnsand, who the first player is, and how the game is won
        If input is incorrect re-opens dialog box
        '''
        dialog = GameInfo()
        dialog.run()

        if dialog.was_done_clicked():
            self._rows = int(dialog.get_row_number())
            self._columns= int(dialog.get_column_number())
            first_player= dialog.get_first_player()
            how_won = dialog.get_how_won()
            if self._rows%2!=0 or self._rows>16 or self._rows<4 or self._columns%2!=0 or self._columns>16 or self._columns<4:
                self._get_input()
            else:
                self._row_col_input = True
            if first_player.lower().strip() != 'b' and first_player.lower().strip() !='w':
                self._get_input()
            else:
                self._first_player_input = True
            if how_won.lower().strip() != 'fewer' and how_won.lower().strip() != 'more':
                self._get_input()
            else:
               self._how_won_input = True 
            if first_player.lower().strip() == 'b' or first_player.lower().strip() == 'black':
                self._first_player = BLACK
            elif first_player.lower().strip() == 'w' or first_player.lower().strip() =='white':
                self._first_player = WHITE

            if how_won.lower().strip() == 'fewer':
                self._how_won = '<'
            elif how_won.lower().strip() == 'more':
                self._how_won = '>'
                
    def _set_up_game(self)-> None:
        '''
        If all input is correct, makes the board (list of lists of empty cells) and deletes the Othello label at the start page
        Makes the grid/gameboard
        Has user set the initial black and white games before the game starts
        '''
        self._get_input()

        if self._row_col_input == True and self._first_player_input== True and self._how_won_input== True:

            self._board = self._make_board()
            self._title_label.destroy()
            self._start_button.destroy()
            
            self._make_grid()
            self._canvas.bind('<Configure>', self._canvas_resized)
            self._set_inital_disks()
        else:
            pass

    def _start_game(self)-> None:
        '''
        Once the inital disks have been places, runs rest of game
        Sets what clicking on the canvas should do
        Creates a gamestate with user input
        Shows the score and who's turn it is
        '''
        self._canvas.bind('<Button-1>', self._canvas_clicked)
        self._gamestate = Gamestate(self._rows,self._columns,self._first_player,self._how_won,self._board)

        self._show_scoreboard()
        self._show_turn(self._gamestate._turn)
        
    def _canvas_clicked(self, event: tkinter.Event)-> None:
        '''
        Once the canvas is clocked, gets row and column number of location of the click
        Makes the turn of desired location
        Adds the disk to the board and creates one on the grid
        While there is no winner, keeps running and sets the next turn
        If the move is invalid or the game is over, does nothung
        '''
        row_index, column_index = self._get_disk_indexes(event)
        try:
            game_board, turn = self._gamestate.verify_move(row_index+1,column_index+1)
            new_disk = Disk(color = self._turn,board_index = (row_index,column_index))
            self._add_disk(new_disk)
            self._add_pieces_from_board(game_board)
            winner = self._gamestate.determine_winner()
            if winner!= None:
                self._show_scoreboard()
                self._determine_winner(winner)
            else:
                if turn == 1:
                    self._turn = BLACK
                elif turn == 2:
                    self._turn = WHITE
                self._show_scoreboard()
                self._show_turn(self._gamestate._turn)
            
        except othello_game_logic.InvalidMoveError:
            pass
        except othello_game_logic.GameOverError:
            pass

    def _determine_winner(self,winner:int):
        '''
        Prints winner to top of window
        '''
        if winner == 1:
            self._header['text'] = 'BLACK WON!'
        elif winner == 2:
            self._header['text'] = 'WHITE WON!'
        elif winner == 0:
            self._header['text'] = 'THE GAME TIED!'

    def _add_pieces_from_board(self,board:[[str,int]]):
        '''
        Changes the board after the move was made so it contains the same disks as the board from game logic
        '''
        for i in range(self._rows):
            for x in range(self._columns):
                if board[i][x]==1:
                    cell = 'black'
                elif board[i][x]==2:
                    cell = 'white'
                elif board[i][x]=='.':
                    cell = '.'
                if self._board[i][x]!=cell:
                    self._board[i][x]=cell
                    d = Disk(color = self._turn,board_index = (i,x))
                    self._add_disk(d)
            

    def _make_board(self)-> None:
        '''
        Initializes board with correct number of rows and columns
        Enters all empty cells
        '''
        board = []
        for i in range(self._rows):
            row = []
            for i in range(self._columns):
                row.append('.')
            board.append(row)
        return board
        
    def _canvas_resized(self,event: tkinter.Event)-> None:
        '''
        Everytime the canvas size changes, redraws the disks and grid to fit current dimensions
        '''
        self._canvas.delete(tkinter.ALL)
        self._make_grid()
        self._print_disks()

    def _show_scoreboard(self)-> None:
        '''
        Gets the amount of black and white disks and displayes the score on the window
        '''
        b_count, w_count = self._gamestate.player_scores()
        scoreboard = tkinter.Label(
            master = self._root_window, text = f'SCORE: Black: {b_count} White: {w_count}', background = 'white',
            font = ('Arial', 20))

        scoreboard.grid(
            row = 2, column = 0, padx = 0, pady = 0,
            sticky = tkinter.S+tkinter.N+tkinter.W+ tkinter.E)

    def _show_turn(self,turn:str)-> None:
        '''
        Displays current player's turn on the top label of the window
        '''
        if turn == 1:
            self._header['text'] = 'Turn: Black'
        if turn == 2:
            self._header['text'] = 'Turn: White'


    def _make_grid(self)-> None:
        '''
        With current canvas dimensions, draws lines for correct number of rows and columns to make grid
        '''
        canvas_width = self._canvas.winfo_width()
        canvas_height = self._canvas.winfo_height()
        column_height = 0
        added_column_distance = canvas_width/self._columns
        for i in range(self._columns+1):
            self._canvas.create_line(column_height, 0, column_height, canvas_height, fill = 'black',width= 4)
            column_height+=added_column_distance

        row_height = 0
        added_row_distance = canvas_height/self._rows
        for i in range(self._rows+1):
            self._canvas.create_line(0, row_height, canvas_width, row_height, fill = 'black',width= 4)
            row_height+=added_row_distance

    def _set_inital_disks(self)-> None:
        '''
        Starts setting disks with the black cells
        '''
        self._board=self._place_initial_black_disks()

    def _place_initial_black_disks(self)-> None:
        '''
        Sets the turn to black
        Displays command on window and creates a done button
        If canvas is clicked, adds black disks
        '''
        self._turn = BLACK
        self._header['text']='Place BLACK disks on board'

        self._canvas.bind('<Button-1>', self._canvas_clicked_inital)

        self._done_button_black = tkinter.Button(master = self._root_window, text = 'Done', font = DEFAULT_FONT,
                                     command = self._initial_disks_done_button_black)

        self._done_button_black.grid(row = 2, column = 0, padx = 10, pady = 10)

        return self._board



    def _initial_disks_done_button_black(self)->[[str]]:
        '''
        Gets rid of done button
        Continues onto setting white disks
        '''
        self._done_button_black.destroy()
        self._place_initial_white_disks()
            

    def _place_initial_white_disks(self)-> None:
        '''
        Sets initial disks for white player
        Creates done button and displays command
        '''
        self._turn = WHITE
        self._header['text']='Place WHITE disks on board'
 
        self._canvas.bind('<Button-1>', self._canvas_clicked_inital)
        self._done_button_white = tkinter.Button(master = self._root_window, text = 'Done', font = DEFAULT_FONT,
                                     command = self._initial_disks_done_button_white)

        self._done_button_white.grid(row = 2, column = 0, padx = 10, pady = 10)

        return self._board

    def _initial_disks_done_button_white(self)->[[str]]:
        '''
        Gets the turn based off the first player and starts the game
        '''
        if self._first_player == BLACK:
            self._turn = BLACK
        elif self._first_player == WHITE:
            self._turn = WHITE
        self._start_game()


    def _get_disk_indexes(self,event:tkinter.Event)->(int,int):
        '''
        Based on click location, determines what location on grid the disk is
        Returs the row and column number of desired location
        '''
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        added_column_distance = width/self._columns
        added_row_distance = height/self._rows
        column = event.x
        row = event.y
        
        row_height = 0
        c = 0
        while row_height <= height:
            if row >= row_height and row<=row_height+added_row_distance:
                row_index = c
                break
            else:
                row_height+=added_row_distance
                c+=1

        column_height = 0
        c = 0
        while column_height <= width:
            if column >= column_height and column<=column_height+added_column_distance:
                column_index = c
                break
            else:
                column_height+=added_column_distance
                c+=1

        return row_index,column_index

    def _canvas_clicked_inital(self,event:tkinter.Event)-> None:
        '''
        Adds a disk anywhere the user clicks
        '''
        row_index,column_index = self._get_disk_indexes(event)
        d = Disk(color = self._turn,board_index = (row_index,column_index))
        self._add_disk(d)

    def _add_disk(self,disk:Disk)-> None:
        '''
        Draws a disk to the grid
        Adds a disk to the list of disks and the board
        '''
        color = self._turn
        self._print_disk(disk,color)
        
        self._disks.append(disk)
        self._board[disk.board_index[0]][disk.board_index[1]]= self._turn

    def _print_disk(self,disk:Disk,color:str)-> None:
        '''
        Based on current dimentions, draws disk to the grid
        '''
        width = self._canvas.winfo_width()
        height = self._canvas.winfo_height()
        added_column_distance = width/self._columns
        added_row_distance = height/self._rows
        column_height = added_column_distance*disk.board_index[1]
        row_height = added_row_distance*disk.board_index[0]

        draw_index = ((column_height+2, row_height,column_height+added_column_distance-2, row_height+added_row_distance))
        self._canvas.create_oval(
                draw_index,
                fill = color, outline = BLACK)

    def _print_disks(self)-> None:
        '''
        Draws all disks currently in game to grid
        '''
        for disk in self._disks:
            self._print_disk(disk,disk.color)



class GameInfo:
    def __init__(self):
        '''
        Initializes dialog window
        Sets labels and entry windows for the user to input the amount of rows, columns, first player, and how the game is won
        Creates a done and cancel button
        '''
        self._dialog_window = tkinter.Toplevel()
        
        input_label = tkinter.Label(
            master = self._dialog_window, text = 'Othello Setup',
            font = DEFAULT_FONT)
            
        input_label.grid(
            row = 0, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.W)

        rows_label = tkinter.Label(
            master = self._dialog_window, text = 'Enter amount of rows (even number between 4-16):',
            font = DEFAULT_FONT)

        rows_label.grid(
            row = 1, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)
        
        self._rows_entry = tkinter.Entry(
            master = self._dialog_window, width = 20, font = DEFAULT_FONT)

        self._rows_entry.grid(
            row = 1, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)

        columns_label = tkinter.Label(
            master = self._dialog_window, text = 'Enter amount of columns (even number between 4-16):',
            font = DEFAULT_FONT)

        columns_label.grid(
            row = 2, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)
        
        self._columns_entry = tkinter.Entry(
            master = self._dialog_window, width = 20, font = DEFAULT_FONT)

        self._columns_entry.grid(
            row = 2, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)
        
        first_player_label = tkinter.Label(
            master = self._dialog_window, text = 'Enter the player you want to move first (B or W):',
            font = DEFAULT_FONT)

        first_player_label.grid(
            row = 3, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)
        
        self._first_player_entry = tkinter.Entry(
            master = self._dialog_window, width = 20, font = DEFAULT_FONT)

        self._first_player_entry.grid(
            row = 3, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)

        how_won_label = tkinter.Label(
            master = self._dialog_window, text = 'Enter if player with more discs or fewer discs will win (more or fewer):',
            font = DEFAULT_FONT)

        how_won_label.grid(
            row = 4, column = 0, padx = 10, pady = 10,
            sticky = tkinter.W)
        
        self._how_won_entry = tkinter.Entry(
            master = self._dialog_window, width = 20, font = DEFAULT_FONT)

        self._how_won_entry.grid(
            row = 4, column = 1, padx = 10, pady = 1,
            sticky = tkinter.W + tkinter.E)

        button_frame = tkinter.Frame(master = self._dialog_window)

        button_frame.grid(
            row = 5, column = 0, columnspan = 2, padx = 10, pady = 10,
            sticky = tkinter.E + tkinter.S)


        done_button = tkinter.Button(master = button_frame, text = 'Done', font = DEFAULT_FONT,
                                     command = self._on_done_button)

        done_button.grid(row = 0, column = 0, padx = 10, pady = 10)

        cancel_button = tkinter.Button(
            master = button_frame, text = 'Cancel', font = DEFAULT_FONT,
            command = self._on_cancel_button)

        cancel_button.grid(row = 0, column = 1, padx = 10, pady = 10)

        self._dialog_window.rowconfigure(5, weight = 1)
        self._dialog_window.columnconfigure(1, weight = 1)

        self._done_clicked = False
        self._row_number = ''
        self._column_number = ''
        self._first_player = ''
        self._how_won = ''

    def run(self)-> None:
        '''
        Runs the dialog window and freezes main window
        '''
        self._dialog_window.grab_set()
        self._dialog_window.wait_window()

    def was_done_clicked(self) -> bool:
        '''
        Returns if the done button was clicked
        '''
        return self._done_clicked
    
    def _on_done_button(self)-> None:
        '''
        If the done button is clicked, sets attribute to true
        Gets the user input and deletes the dialog window
        '''
        self._done_clicked = True
        self._row_number = self._rows_entry.get()
        self._column_number = self._columns_entry.get()
        self._first_player = self._first_player_entry.get()
        self._how_won = self._how_won_entry.get()
        self._dialog_window.destroy()

    def _on_cancel_button(self) -> None:
        '''
        If the cancel button is pressed, deletes the dialog window
        '''
        self._dialog_window.destroy()

    def get_row_number(self)-> str:
        '''
        Returns the row number
        '''
        return self._row_number
    
    def get_column_number(self)-> str:
        '''
        Returns the column number
        '''
        return self._column_number

    def get_first_player(self)->str:
        '''
        Returns the first player
        '''
        return self._first_player

    def get_how_won(self)->str:
        '''
        Returns how the game is won
        '''
        return self._how_won


if __name__ == '__main__':
    game = Othello()
    game.run_game()
