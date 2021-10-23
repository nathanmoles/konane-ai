from gameBoard import Board
import copy
import random
import time
import sys

static_eval_count = 0
num_calls = 0
total_branches = 0
cutoffs = 0

def minimax(game_state, depth_bound):
	global num_calls
	global total_branches
	global static_eval_count
	global cutoffs

	if depth_bound == 3:
		static_eval_count += 1
                return (game_state.static_evaluation(), None) 	# Node evaluation
		
        if game_state.current_player == 0:	# max function
		bestmove = None
		num_calls += 1
		value = float('-inf')

		for successor_game_state in game_state.generate_successors():
                        total_branches += 1

			newVal, move = minimax(successor_game_state, depth_bound+1)
			
			if newVal > value:
				value = newVal
				bestmove = successor_game_state.last_move_made
		return (value, bestmove)
        else: 	# min function
		bestmove = None
		num_calls += 1

		value = float('inf')

		for successor_game_state in game_state.generate_successors():
                        total_branches += 1

			newVal, move = minimax(successor_game_state, depth_bound+1)
			
			if newVal < value:
				value = newVal
				bestmove = successor_game_state.last_move_made

		return (value, bestmove)
	return


def alphabeta(game_state, alpha, beta, depth_bound):
	global num_calls
	global total_branches
	global static_eval_count
	global cutoffs



        if depth_bound == 1:
		static_eval_count += 1
                return (game_state.static_evaluation(), None) 	# Evaluation of the leaf node
		
        elif game_state.current_player == 0:	# Max function
		bestmove = None
		num_calls += 1

		for successor_game_state in game_state.generate_successors():
                        total_branches += 1


			bv, player_move = alphabeta(successor_game_state, alpha, beta, depth_bound+1)
			
			if alpha >= beta:
				cutoffs +=1
				return (beta, bestmove)

			if bv > alpha:
				alpha = bv
				bestmove = successor_game_state.last_move_made

		return (alpha, bestmove)
        else: 	# Min function
		bestmove = None
		num_calls += 1

		for successor_game_state in game_state.generate_successors():
			total_branches += 1

			bv, computer_move = alphabeta(successor_game_state, alpha, beta, depth_bound+1)

			if beta <= alpha:
				cutoffs +=1
				return (alpha, bestmove)

			if bv < beta:
				beta = bv
				bestmove = successor_game_state.last_move_made

		return (beta, bestmove)

class Game:
	def __init__(self, board_size, board, player=0, last_move_made = ((),())):
		self.board_size = board_size
		self.board = board
		self.last_move_made = last_move_made
		self.current_player = player
		self.player_symbol = ('B','W')
		self.endgame = 0

	def get_legal_moves(self, current_player):
                """ Gets list of moves possible in state"""
		legal_moves = []

		for row in range(self.board_size):
			for col in range(self.board_size):

				if self.board.repr[row][col] == self.player_symbol[current_player]:
					position  = (row,col)
                                        move_fn_list = [self.north_move, self.east_move, self.south_move, self.west_move]

					for move_fn in move_fn_list:
						move = move_fn(position)

						if self.is_legal_move(current_player,move):
					 		legal_moves.append(move)

                                                        start = move[0]
					 		cur_end   = move[1]

                                                        new_board = copy.deepcopy(self.board)

                                                        # Checking double jump possibility

					 		new_board.movePiece(start,cur_end)

                                                        continue_move = move_fn(cur_end)
                                                        new_game_state = Game(self.board_size,new_board,current_player)

					 		while(new_game_state.is_legal_move(current_player, continue_move)):
					 			start_cur = cur_end
					 			cur_end = continue_move[1]
					 			legal_moves.append((start,cur_end))

						 		new_board = copy.deepcopy(new_board)
					 			new_board.movePiece(start_cur,cur_end)

					 			continue_move = move_fn(cur_end)
					 			new_game_state = Game(new_game_state.board_size,new_board,current_player)
		return legal_moves

	def is_legal_move(self, current_player, move):
                """ Checking if move is possible """
		starting_pos = move[0]
		ending_pos   = move[1]

                #testing end range
                if ending_pos[0] not in range(self.board_size) or ending_pos[1] not in range(self.board_size):
			return False 

                if self.board.repr[starting_pos[0]][starting_pos[1]]!=self.player_symbol[current_player]:
			return False

                # Making sure spot moved to is empty
                if self.board.repr[ending_pos[0]][ending_pos[1]]!= ' ':
			return False

                middle_pos = (starting_pos[0]-(starting_pos[0]-ending_pos[0])/2,starting_pos[1]-(starting_pos[1]-ending_pos[1])/2)
		other_player = 1 - current_player 

		if self.board.repr[middle_pos[0]][middle_pos[1]] != self.player_symbol[other_player]:
			return False 
		return True

        def generate_successors(self): # generating possible states
		successors = []

		for move in self.get_legal_moves(self.current_player):
			boardCopy = copy.deepcopy(self.board)
			boardCopy.movePiece(move[0], move[1])
			successors.append(Game(self.board_size, boardCopy, 1-self.current_player, move))

		for s in successors:
			if False:
				print (s.board)
		return successors

        def minimax_turn(self, isAlphaBeta):# doing minimax Algo
		global num_calls

		if len(self.get_legal_moves(self.current_player)) != 0:
			if (isAlphaBeta):
				computer_move = alphabeta(self, float("-inf"), float("inf"), 0)
			else:
				computer_move = minimax(self,  0)
			computer_move = computer_move[1]

			print(self.board)

			if computer_move is not None:
				self.board.movePiece(computer_move[0], computer_move[1])
				
				print(self.board)

				self.last_move_made = computer_move
				self.current_player = 1 - self.current_player

			else:
				random_move =  random.choice(self.get_legal_moves(self.current_player))
				self.board.movePiece(random_move[0], random_move[1])

				print(self.board)

				self.last_move_made = computer_move
				self.current_player = 1 - self.current_player
		else:
			self.endgame = 1
			print("Player", self.player_symbol[self.current_player], "loses!")

        def random_turn(self): # random agent algo
		if len(self.get_legal_moves(self.current_player)) != 0:
			random_move =  random.choice(self.get_legal_moves(self.current_player))
			self.board.movePiece(random_move[0], random_move[1])

			print(self.board)

			self.last_move_made = random_move
			self.current_player = 1 - self.current_player
		else:
			self.endgame = 1
			print("Player", self.player_symbol[self.current_player], "loses!")

        # Piece moving methods
	@staticmethod
	def north_move(pos):
		return (pos,(pos[0]-2,pos[1]))


	@staticmethod
	def east_move(pos):
		return (pos,(pos[0],pos[1]+2))



	@staticmethod
	def south_move(pos):
		return (pos,(pos[0]+2,pos[1]))


	@staticmethod
	def west_move(pos):
		return (pos,(pos[0],pos[1]-2))


	def static_evaluation(self):
                # evaluating the possible moves

		my_moves = self.get_legal_moves(0)

		opponent_moves = self.get_legal_moves(1)

		if opponent_moves == 0:
			return float("inf")

		if my_moves == 0:
			return float("-inf")

                #returning the difference in length of moves so that biggest difference is chosen
		return len(my_moves) - len(opponent_moves)

def test_game(game_state):
	game_state.board.removePiece((3,3))
	print(game_state.board)

	game_state.board.removePiece((3,2))
	print(game_state.board)

	while game_state.endgame != 1:
		if game_state.current_player == 0:
			game_state.minimax_turn(False)
		else:
			game_state.random_turn()


if __name__ == '__main__':

        test_game(Game(8,Board(8))) #running game
        print("Static Evals: ", static_eval_count)
        print("Branching Factor: ", total_branches/(num_calls+0.0))
        print("Cutoffs: ", cutoffs)
