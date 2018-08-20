#othello_game_logic.py
#Alexandra Movsesyan
#42206297

Black = 1
White = 2

class InvalidMoveError(Exception):
    '''
    Raised whenever an invalid move is made
    '''
    pass

class GameOverError(Exception):
    '''
    Raised whenever an attempt is made to make a move after the game is
    already over
    '''
    pass

class Gamestate:
    
    def __init__(self,rows:int,columns:int,first_player:str,how_won:str,user_board:[str])->[[str]]:
        '''
        Initializes a Gamestate and based on the user input stores:
            the board, amount of columns, amount of rows, how the game is won, and first player
        Also determines opposite player, and creates a winner
        '''
        self._make_board(rows,columns,user_board)
        self._columns = columns
        self._rows = rows
        self._how_won = how_won
        turn = first_player


        if turn == 'black':
            self._turn = Black
            self._opposite_player = White
        elif turn == 'white':
            self._turn = White
            self._opposite_player = Black
        self._winner = None


    def verify_move(self,row:int,col:int)->([[str]],int):
        '''
        Verifies if the moves is valid, then executes move
        Raises InvalidMoveError if the cell is already occupied, there are no valid mores,
        or the row or column number do not exist
        '''
        try:
            if self._check_space_empty(row,col) == False:
                    raise InvalidMoveError()
            else:
                self._get_valid_moves()
                if self._moves == []:
                    raise InvalidMoveError()
                else:
                    self._make_moves()
                    self._determine_turn()
                    return self._board,self._turn
        except IndexError:
            raise InvalidMoveError()

    def player_scores(self)->(int,int):
        '''
        Based on the cells in the board, determines amount of Black and White cells and returns count
        '''
        self._b_count = 0
        self._w_count = 0
        for row in self._board:
            for item in row:
                if item == 1:
                    self._b_count +=1
                elif item == 2:
                    self._w_count +=1
        return self._b_count,self._w_count

    def determine_winner(self)-> None:
        '''
        Checks if there are any more valid moves avaiable
        If there are, there is not winner
        If there aren't any valid moves, determines winner based on how the user
        wanted the game to be won, using the amount of black and white cells
        '''
        if self._determine_if_valid_moves_still_available() == False:
            b_count, w_count = self.player_scores()
            if b_count == w_count:
                winner = 0
            elif self._how_won == '>':
                if b_count > w_count:
                    winner = Black
                elif w_count > b_count:
                    winner = White
            elif self._how_won == '<':
                if b_count > w_count:
                    winner = White
                elif w_count > b_count:
                    winner = Black
        else:
            winner = None
        self._winner = winner
        return winner
        

    def _make_board(self,rows:int,columns:int,user_board:[[str]])-> None:
        '''
        Makes a board based on user input
        '''
        board = []
        for x in range(rows):
            board.append([])
        c = 0
        while c < rows:
            new_row = []
            for item in user_board[c]:
                if item == 'black':
                    new_row.append(Black)
                elif item == 'white':
                    new_row.append(White)
                elif item == '.':
                    new_row.append('.')
            board[c] = new_row
            c+=1
        self._board= board

    def _find_valid_indexes(self)->[(int,int)]:
        '''
        Searches through the board and findes every blank cell
        '''
        indexes = []
        i = 0
        while i < self._rows:
                row = list(enumerate(self._board[i]))
                c = 0
                while c < len(row):
                        if row[c][1]== '.':
                                index = (i,c)
                                indexes.append(index)
                        c+=1
                i+=1
        self._valid_indexes = indexes

    def _find_if_valid_moves(self,current_player:int,opposite_player:int)-> None:
        '''
        Determines if any blank cell could be a valid move
        '''
        valid_moves = False
        i = 0
        while i <len(self._valid_indexes):
            self._row_number = self._valid_indexes[i][0]
            self._column_number = self._valid_indexes[i][1]
            self._get_valid_moves()
            if self._moves != []:
                valid_moves = True
                break
            elif self._moves == []:
                pass
            i+=1
                    
        return valid_moves

 
    def _determine_turn(self)->str:
        '''
        Based on the valid indexes, swithces the current player and opposite player
        If the opposite player has no valid moves, turn reverts back to current player
        '''
        self._find_valid_indexes()
        if self._turn == Black:
            self._turn = White
            self._opposite_player = Black
            
            white_valid_moves = self._find_if_valid_moves(self._turn,self._opposite_player)
            if white_valid_moves == False:
                self._turn = Black
                self._opposite_player = White

        elif self._turn == White:
            self._turn = Black
            self._opposite_player = White

            black_valid_moves = self._find_if_valid_moves(self._turn,self._opposite_player)
            if black_valid_moves == False:
                self._turn = White
                self._opposite_player = Black
        return self._turn

    
    def _determine_if_valid_moves_still_available(self)->bool:
        '''
        Checks if there are any valid moves still available for both players
        '''
        black_moves = self._find_if_valid_moves(Black,White)
        white_moves = self._find_if_valid_moves(White,Black)
        if white_moves == False and black_moves == False:
            return False

    def _check_space_empty(self,row:int,column:int)-> bool:
        '''
        Given a cell location, determines if it is empty
        '''
        self._row_number = row-1
        self._column_number = column-1

        if self._board[self._row_number][self._column_number]== '.':
            return True
        else:
            return False
        

    def _get_valid_moves(self)-> [str]:
        '''
        Checks if there are any valid moves in horizontal, vertical, and diagonal direction
        Creates starting and ending indexes for the cells to flip in that certain valid move
        '''
        valid_moves = []
        if self._check_vertical()== True:
            valid_moves.append('v')
            self._start_index_v = self._starting_index
            self._end_index_v = self._ending_index
            
        if self._check_horizontal()== True:
            valid_moves.append('h')
            self._start_index_h = self._starting_index
            self._end_index_h = self._ending_index
            
        if self._check_diagonal_forward()== True:
            valid_moves.append('d1')
            self._start_index_d1 = self._starting_index
            self._end_index_d1 = self._ending_index
            
        if self._check_diagonal_backward()== True:
            valid_moves.append('d2')
            self._start_index_d2 = self._starting_index
            self._end_index_d2 = self._ending_index
        self._moves = valid_moves
    
    
            
    def _make_moves(self)-> None:
        '''
        Executes all valid moves
        '''
        if self._winner!= None:
            raise GamveOverError()
        for move in self._moves:
            if move == 'h':
                board = self._horizontal_move()
            elif move == 'v':
                board = self._vertical_move()
            elif move == 'd1':
                board = self._diagonal_forwards_move()
            elif move == 'd2':
                board = self._diagonal_backwards_move() 
    


    def _check_if_valid(self)-> None:
        '''
        With a given line(horizontal, vertical, or diagonal) checks if move is valid
        Immidately becomes invalid if the opposite player doesnt have a cell in that line
        Finds the instances of the current player in the line and determines the starting
        and ending indexes of which the cells should be flipped
        Move is invalid if the opposite player insn't in-between those indexes
        '''
        if self._turn not in self._area_to_check:
            return False
        
        c =0
        while c < len(self._area_to_check):
            if self._area_to_check[c] == self._turn:
                last_instance = c
            else:
                pass
            c+=1

        i =0
        while i < len(self._area_to_check):
            if self._area_to_check[i] == self._turn:
                first_instance = i
                break
            i+=1
        if first_instance <self._new_index:
            trajectory = self._area_to_check[first_instance:(self._new_index+1)]
            if self._opposite_player in trajectory:
                self._starting_index = first_instance
                self._ending_index = self._new_index
                return True
            else:
                return False

        elif first_instance > self._new_index:
            trajectory = self._area_to_check[self._new_index:(last_instance+1)]
            if self._opposite_player in trajectory:
                self._starting_index = self._new_index
                self._ending_index = last_instance
                return True
            else:
                return False
        
    def _check_horizontal(self)->bool:
        '''
        Finds a horizontal line based on desired cell placement
        Checks if a horizontal move is valid
        '''
        horizontal = self._board[self._row_number]
        self._new_index = self._column_number
        self._area_to_check = horizontal

        response = self._check_if_valid()
        return response


    def _check_vertical(self)-> None:
        '''
        Finds a vertical line based on desired cell placement
        Checks if a vertical move is valid
        '''
        self._new_index = self._row_number
        vertical = []
        
        row = 0
        while row < len(self._board):
            vertical.append(self._board[row][self._column_number])
            row+=1
        self._area_to_check = vertical

        response = self._check_if_valid()
        return response

    def _check_diagonal_forward(self)-> None:
        '''
        Finds a forwards diagonal line based on desired cell placement
        Checks if a forwards diagonal move is valid
        '''
        self._new_index = self._row_number
        diagonal1 = self._get_diagonal_forward()
        self._area_to_check = diagonal1
        response = self._check_if_valid()
        return response

    def _check_diagonal_backward(self)-> None:
        '''
        Finds a backwards diagonal line based on desired cell placement
        Checks if a backwards diagonal move is valid
        '''
        self._new_index = self._row_number
        diagonal2 = self._get_diagonal_backwards()
        self._area_to_check = diagonal2
        response = self._check_if_valid()
        return response
        
    def _get_diagonal_forward(self)->[int,str]:
        '''
        Generates a forwards diagonal line based on desired indexes
        '''
        diagonal = []
        row = self._row_number
        col = self._column_number
        
        while row >= 0 and col >= 0:
            diagonal.append(self._board[row][col])
            row-=1
            col-=1
        diagonal.reverse()
        
        row = self._row_number
        col = self._column_number
        while row < self._rows-1 and col < self._columns-1:
            diagonal.append(self._board[row+1][col+1])
            row+=1
            col+=1

        return diagonal

    def _get_diagonal_backwards(self)->[int,str]:
        '''
        Generates a backwards diagonal line based on desired indexes
        '''
        diagonal = []
        row = self._row_number
        col = self._column_number
        while row >= 0 and col < self._columns:
            diagonal.append(self._board[row][col])
            row-=1
            col+=1
        diagonal.reverse()
        
        row = self._row_number
        col = self._column_number
        while row < self._rows-1 and col >0:
            diagonal.append(self._board[row+1][col-1])
            row+=1
            col-=1

        return diagonal

    def _horizontal_move(self)->[[int,str]]:
        '''
        With a starting and ending index, flips all cells in a horizontal line to the current player
        '''
        start = self._start_index_h

        while start <= self._end_index_h:
            self._board[self._row_number][start] = self._turn
            start+=1
        return self._board

    def _vertical_move(self)->[[int,str]]:
        '''
        With a starting and ending index, flips all cells in a vertical line to the current player
        '''
        start = self._start_index_v

        while start <= self._end_index_v:
            self._board[start][self._column_number] = self._turn
            start+=1

        return self._board

    def _diagonal_forwards_move(self)->[[int,str]]:
        '''
        With a starting and ending index, flips all cells in a forwards diagonal line to the current player
        '''
        start = self._start_index_d1

        if start == self._row_number:
            row = start
            col = self._column_number
            while row <=self._end_index_d1:
                self._board[row][col] = self._turn
                row+=1
                col+=1

        elif start != self._row_number:
            row = self._end_index_d1
            col =self._column_number
            while row >=self._start_index_d1:
                self._board[row][col] = self._turn
                row-=1
                col-=1

        return self._board

    def _diagonal_backwards_move(self)->[[int,str]]:
        '''
        With a starting and ending index, flips all cells in a backwards diagonal line to the current player
        '''
        start = self._start_index_d2

        if start == self._row_number:
            row = start
            col = self._column_number
            while row <=self._end_index_d2:
                self._board[row][col] = self._turn
                row+=1
                col-=1

        elif start != self._row_number:
            row = self._end_index_d2
            col =self._column_number
            while row >=self._start_index_d2 and col<= self._columns-1:
                self._board[row][col] = self._turn
                row-=1
                col+=1

        return self._board
