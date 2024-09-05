import math
from copy import deepcopy, copy

class Tileset:
    tiles = [[0,0,0],[0,0,0],[0,0,0]] #By default, create a tileset of 0's
    empty_tile = [0,0] #By default, the empty tile is the first
    def __init__(self, new_tiles, initial_empty): #When creating a tile set
        self.tiles = new_tiles #Parse the first argument as the tiles
        self.empty_tile = initial_empty #Parse the second argument as the empty tile location
    def show_tiles(self):
        return self.tiles #Return the tiles of a tile set
    def move_tile(self, coords): #Move the tile at the specified co-ordinates to the empty space
        new_tiles = deepcopy(self)
        new_tiles.tiles[new_tiles.empty_tile[0]][new_tiles.empty_tile[1]] = new_tiles.tiles[coords[0]][coords[1]] #Set the empty tile to contain the tile to move
        new_tiles.empty_tile = [coords[0], coords[1]] #Set the co-ordinates of the now empty tile to the location of the tile to move
        new_tiles.tiles[coords[0]][coords[1]] = 0 #Set the tile to move to be empty
        return new_tiles
    def get_valid_moves(self): #Returns a list of all possible move co-ordinates for a tile
        empty_tile = self.empty_tile
        possible_moves = []
        if((empty_tile[0] - 1) > -1): #Check if a move is in range of the list
            possible_moves.append([empty_tile[0] - 1, empty_tile[1]]) #Append it if it is
        if((empty_tile[0] + 1) < 3):
            possible_moves.append([empty_tile[0] + 1, empty_tile[1]])
        if((empty_tile[1] - 1) > -1):
            possible_moves.append([empty_tile[0], empty_tile[1] - 1]) 
        if((empty_tile[1] + 1) < 3):
            possible_moves.append([empty_tile[0], empty_tile[1] + 1])
        return possible_moves

class Node:
    node_tile_set = Tileset([],[])
    score = 0
    path = []
    goal_tile_set = Tileset([],[])
    def __init__(self, new_tile_set, new_path, new_h, score, goal_tile_set):
        self.node_tile_set = new_tile_set
        self.path = new_path
        self.heuristic = new_h
        self.score = score
        self.goal_tile_set = goal_tile_set
    def get_node_neighbours(s):
        node_neighbours = [] #Create an empty list of node neighbours
        moves = s.node_tile_set.get_valid_moves() #Get the valid possible moves
        for move in moves: #For each of those moves
            new_tiles = deepcopy(s.node_tile_set).move_tile(move) #Copy the tile set, and move the tile in the specific way
            new_moves = copy(s.path) #Copy the path of the current node
            new_moves.append(move) #Append the move to the end of the current path
            new_node = Node(new_tiles, new_moves, s.heuristic, s.score + get_score(new_tiles, s.goal_tile_set, s.heuristic), s.goal_tile_set) #Create a new node with newly generated properties
            node_neighbours.append(new_node) #Add it to the list of node neighbours
        return node_neighbours
    def check_if_goal(self): #Check if this node is the same as its goal
        return check_same(self.node_tile_set, self.goal_tile_set)
    
def check_same(one_set, two_set): #Check if two tile sets are the same
    return (one_set.show_tiles() == two_set.show_tiles())

def get_destination(num_to_find, goal_state): #Return the co-ordinates of the given number within the goal state
    row = 0
    col = 0
    for i in range(0,3): #For each row
        for j in range(0,3): #For each tile in that row
            if(num_to_find == goal_state[i][j]): #Check if the number at that tile is equal to the number to search for
                row = i #If it is, mark the row and column
                col = j 
    return [row, col] #Return the row and column as a pair of co-ordinates
    
def get_score(start_state, goal_state, heuristic): #Get the score of a given state
    current_score = 0
    for i in range(0,3): #For every row
        for j in range(0,3): #For every tile in that row
            number_in_state = start_state.show_tiles()[i][j] #Get the number in that tile
            goal_coords = get_destination(number_in_state, goal_state.show_tiles()) #Get the co-ordinates that the tile should be aiming for
            if(heuristic == "man"):
                current_score += get_manhattan([i, j], goal_coords)
            else:
                current_score += get_euclidean([i, j], goal_coords)
    return current_score

def get_manhattan(coords, goal_coords): #Returns the Manhattan distance between two sets of co-ordinates as an integer
    xdif = abs(coords[0] - goal_coords[0]) #Get the difference in value between the co-ordinates
    ydif = abs(coords[1] - goal_coords[1])
    return (xdif + ydif) #Return the sum of these two differences
    
def get_euclidean(coords, goal_coords): #Returns the Euclidean distance between two sets of co-ordinates as an integer
    return math.sqrt(((coords[0] - goal_coords[0])**2) + ((coords[1] - goal_coords[1])**2))

def find_lowest_node(node_list):
    lowest_dist = 1000 #Works as infinity
    lowest_index = 0
    for node_index in range(0,len(node_list)): #For every node in the node array
        if(node_list[node_index].score < lowest_dist): #If it is the lowest node
            lowest_dist = node_list[node_index].score #Set the new minimum distance
            lowest_index = node_index #Set the new lowest index
    return lowest_index
    
def check_node_presence(new_node, node_list):
    for index in range(0,len(node_list)): #For every node in the node list
        if(node_list[index].node_tile_set.show_tiles() == new_node.node_tile_set.show_tiles()): #If the tile set is the same
            return True #Return true that the tileset is in the list
    return False #Return False if the node is not found within the list
    
def better_node_check(new_node, node_list):
    better_index = -1 #Say that you have not yet found a better index
    for index in range(0, len(node_list)): #For each index
        if(node_list[index].node_tile_set.show_tiles() == new_node.node_tile_set.show_tiles()): #If the tile sets are the same
            if(node_list[index].score < new_node.score): #If the new node has a better score
                better_index = index #Set the index to replace
    return better_index
    
def create_path(start_state, goal_state, heuristic):
    start_node = Node(start_state, [], heuristic, 0, goal_state)
    new_nodes = [start_node]
    explored_nodes = []
    node_exploration_count = 0
    while (len(new_nodes) > 0): #Whilst there are new nodes to search
        lowest_node = new_nodes[find_lowest_node(new_nodes)] #Get the the lowest node
        new_nodes.remove(lowest_node) #Remove the node from the list of new nodes
        explored_nodes.append(lowest_node) #And append it to the list of explored nodes
        node_exploration_count += 1
        if lowest_node.check_if_goal(): #If the node is the goal
            print(node_exploration_count, "different nodes were explored until the solution was reached.") #Print the number of explored nodes
            return lowest_node #Return it
        else: #Otherwise
            for neighbour in lowest_node.get_node_neighbours(): #For every neighbouring node
                if not check_node_presence(neighbour, explored_nodes): #Check that it has not been found before
                    better_index = better_node_check(neighbour, new_nodes) #Check if this new node is a better path to a neighbour that a previously found path
                    if(better_index != -1): #If it does
                        new_nodes[better_index] = neighbour #Replace the node with the better path
                    else: #Otherwise
                        new_nodes.append(neighbour) #Append the neighbour if it has not been found

def get_player_input():
    user_list = [] #Create an empty list
    while(len(user_list)<3): #Whilst there are less than 3 inputted rows
        input_string = input()
        input_line = [] #Create an empty list to represent the input line
        valid_line = True #Say that the input is currently valid
        for char in input_string: #For each character the user inputted
            if not (char.isdigit()): #Check it is a digit
                valid_line = False
                print("A non-number was detected in the input")
            else:
                input_line.append(int(char)) #Add it to the list if it is
        if(len(input_line) != 3): #Check the input is the right length
            valid_line = False
            print("Incorrect number of inputs")
        if(valid_line):
            user_list.append(input_line) #Add the inputted row to the list
    return user_list

def validate_input(input_list):
    valid_numbers = []
    for i in range(9): #Add the numbers 0-8 to a list
        valid_numbers.append(i)
    valid_input = True #Mark the input as currently true
    for line in input_list: #Iterate through the inputted line
        for cur_num in line: 
            if cur_num in valid_numbers: #Removing a number from the valid numbers when it is found
                valid_numbers.remove(cur_num)
            else: #Mark an input as invalid if there is a duplicate
                valid_input = False
    if not (valid_input): #Display an error message if an input is invalid
        print("The numbers 0-8 have not been uniquely found within the input")
    return valid_input
    
def find_zero_tile(input_list): #Finds a zero tile in an inputted list
    for row in range(3):
        for column in range(0,3):
            if (input_list[row][column] == 0):
                return [row, column]

goal_state = Tileset([[0,1,2],[3,4,5],[6,7,8]], [0,0]) #Create the goal state
start_state = Tileset([[7,2,4],[5,0,6],[8,3,1]], [1,1]) #Create the default start state
print("Enter y if you would like to use a custom start state") #Ask for a custom start state
custom_state = input()
if(custom_state == "y"):
    valid_input = False #Mark that no valid input has been enterred
    while(valid_input == False): #Whilst a valid input has not been entered
        print("Use 0 for the empty tile")
        print("Please enter three rows in the format XYZ (Eg 123): ") #Ask for an input
        input_list = get_player_input() #Ask for an input
        if (validate_input(input_list)): #Check it is valid
            valid_input = True #Mark that it is valid
            start_state = Tileset(input_list, find_zero_tile(input_list)) #Create a tileset from the input
print("Enter y if you would like to use a custom goal state") #Ask for a custom start state
custom_state = input()
if(custom_state == "y"):
    valid_input = False #Mark that no valid input has been enterred
    while(valid_input == False): #Whilst a valid input has not been entered
        print("Use 0 for the empty tile")
        print("Please enter three rows in the format XYZ (Eg 123): ") #Ask for an input
        input_list = get_player_input() #Ask for an input
        if (validate_input(input_list)): #Check it is valid
            valid_input = True #Mark that it is valid
            goal_state = Tileset(input_list, find_zero_tile(input_list)) #Create a tileset from the input
print("Please enter \'man\' to use manhattan distance, or anything else for euclidean distance")
option = input()
finalNode = create_path(start_state, goal_state, option)
print("Reaching the final node required", len(finalNode.path), "moves")
print("Type y to display the path to the node")
option = input()
if(option == "y"):
    print("Start state:") #Print the start state
    print(start_state.show_tiles()[0])
    print(start_state.show_tiles()[1])
    print(start_state.show_tiles()[2])
    for move in finalNode.path: #For every move in the path of the final node
        start_state = start_state.move_tile(move) #Make the move
        print("Next step:") 
        for row in start_state.show_tiles(): #Print each row from the resulting move
            print(row)