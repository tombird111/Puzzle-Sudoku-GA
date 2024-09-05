from random import choice, random, randrange, seed
from copy import deepcopy

class Row:
    row = [0,0,0,0,0,0,0,0,0]
    fixed_indexes = []
    fixed_numbers = []
    def __init__(self, new_row):
        read_info = self.read_row(new_row)
        self.row = read_info[0]
        self.fixed_indexes = read_info[1]
        self.fixed_numbers = read_info[2]
        self.randomise_row()
    def read_row(self, row_string): #Constructs a row from an input string
        division_count = 0;
        read_info = []
        row = [0,0,0,0,0,0,0,0,0]
        fixed_indexes = []
        fixed_numbers = []
        for current_index in range(len(row_string)): #For every character in the input string
            if(row_string[current_index] == '!'): #If it is a !
                division_count += 1 #Add 1 to the division count
            elif(row_string[current_index].isdigit()): #If the character is a digit
                number = int(row_string[current_index]) #Cast an integer from the digit
                if(number > 0): #If the number is not a 0
                    row[current_index - division_count] = number #Set the number in the row to match
                    fixed_numbers.append(number) #Add the number to a list of numbers
                    fixed_indexes.append(current_index - division_count) #Add the index of the number to the list of fixed indexes
                else:
                    print("0 found within input");
        read_info.append(row)
        read_info.append(fixed_indexes)
        read_info.append(fixed_numbers)
        return read_info
    def randomise_row(self):
        numbers_to_place = []
        for i in range(1,10): #For numbers 1 to 9
            if not (i in self.fixed_numbers): #If the number is not in the row
                numbers_to_place.append(i) #Append the number to a list of numbers to place
        for index in range(len(self.row)): #For each index in the row
            if not (index in self.fixed_indexes): #If the index is not a fixed index
                num_to_add = choice(numbers_to_place) #Choose a random number from the numbers to add
                self.row[index] = num_to_add #Set the chosen index to contain the chosen number
                numbers_to_place.remove(num_to_add) #Remove the chosen number from the list of numbers to place

class Puzzle:
    rows = []
    def __init__(self, new_rows):
        self.rows = new_rows
    def print_puzzle(self):
        for row in self.rows:
            print(row.row)
    def get_fitness(self):
        collision_count = 0
        collision_count += self.column_check() #Count the number of errors within each column
        collision_count += self.square_check() #Count the number of errors within each 3X3 square
        return (81 - collision_count) #Return 81 - the number of errors
    def column_check(self):
        errors = 0
        for column_index in range(len(self.rows)): #For each possible column
            found_numbers = [] #Say that no numbers have been found
            for row_index in range(len(self.rows)):
                if self.rows[row_index].row[column_index] in found_numbers: #If the number found at the space within the column has already been found
                    errors += 1 #Say that an error has been found
                else: #Otherwise
                    found_numbers.append(self.rows[row_index].row[column_index]) #Add the number to the list of numbers found within the column
        return errors
    def square_check(self):
        errors = 0
        squares = self.create_squares()
        for square in squares: #For every square in the puzzle
            found_numbers = [] #Create a list of currently found numbers
            for i in range(3): #For every number in the square
                for j in range(3):
                    if square[i][j] in found_numbers: #Check that it has been found before
                        errors += 1 #If it has been found, increase the number of errors
                    else: #Otherwise
                        found_numbers.append(square[i][j]) #Append the number to the list of found numbers
        return errors
    def create_squares(self):
        squares = []
        for i in range(0,6,3): #For 0, 3, 6
            for j in range(0,6,3): #For 0, 3, 6
                squares.append(self.create_square(i, j)) #Create a square from that position
        return squares #Return the squares
    def create_square(self, row_start, column_start):
        square = [] #Create an empty square
        for i in range(3): #For 0, 1, 2
            row = [] #Create an empty row
            for j in range(3): #For 0, 1, 2
                row.append(self.rows[row_start + i].row[column_start + j]) #Append the next 3 numbers based on the position in the puzzle 
            square.append(row) #Append the row to the square
        return square #Return the square
    def mutate(self):
        index = randrange(0,9) #Pick a random row
        self.rows[index].randomise_row() #Randomise it
        
#Population control functions

def populate(pop_num, input_strings): #Creates a list of puzzles based on an inputted list of strings and returns it
    population = []
    for i in range(pop_num): #Create a number of puzzles based on the inputted number
        population.append(create_pop(input_strings))
    return population

def create_pop(input_strings): #Create a single puzzle based on a list of strings, and returns it
    new_puzzle = []
    for string in input_strings: #For every string in the list
        new_puzzle.append(Row(string)) #Create a row from that string, and append it
    return Puzzle(new_puzzle)
    
    
#Individual control functions
def crossover(puzzle_list): #Recieves a list of two parents then constructs and returns a child based on those parents
    new_puzzle = [] #Create an empty list
    for i in range(0,9): #For the range 0-8
        pick = randrange(0,2) #Pick 0 or 1
        new_puzzle.append(puzzle_list[pick].rows[i]) #Add the row from either parent based on the random number
    return Puzzle(new_puzzle) #Return the child

def mutate(puzzle, mutation_strength): #Takes a puzzle, and mutates it to a degree equal to the mutation strength
    for i in range(mutation_strength): #For each level of mutation strength
        puzzle.mutate() #Mutate the puzzle
    
#Generation control functions
def get_next_generation(puzzle_list):
    new_generation = []
    for puzzle in selection(puzzle_list): #Append the top 50% of puzzles to an asexual group
        new_generation.append(puzzle)
    index = 0 #Starting from the first index
    while len(new_generation) < len(puzzle_list): #Whilst the generation has not been filled
        if(index + 1 > len(new_generation)): #If the index would go over the range of the array
            index = 0 #Set it back to 0
        elif(len(new_generation) == 1): #If the new generation has a new generation of 1 (only for testing purposes)
            new_generation.append(new_generation[0]) #Add a copy of the item to the new generation
        else: #Otherwise
            new_generation.append(crossover([new_generation[index], new_generation[index + 1]])) #Add a child of two adjacent parents
            index += 1 #Move the index on by 1
    return new_generation #Return the new generation
    
def selection(puzzle_list):
    new_list = [] #Create a new empty list
    average = get_average_fitness(puzzle_list) #Get the average fitness
    for puzzle in puzzle_list: #For each puzzle in the list
        if (puzzle.get_fitness() >= average): #If it has greater than average fitness
            new_list.append(puzzle) #Append it to the list
    return new_list #Return the list
    
def tournament_selection(puzzle_list):
    new_list = [] #Create a new empty list
    for index in range(0, len(puzzle_list), 4): #For every index in the puzzle list, going by steps of 4
        tournament = [] #Create an empty tournament
        for i in range(4): #Append the next 4 puzzles within range to the tournament
            if (index + i < len(puzzle_list)):
                tournament.append(puzzle_list[index + i])
        best_competitor = tournament[0] #Note the best competitor as the first
        for competitor in tournament: #For each competitor
            if (competitor.get_fitness() > best_competitor.get_fitness()): #If it possesses a better fitness than the current best
                best_competitor = competitor #Choose that competitor as the new best competitor
        new_list.append(best_competitor) #Append the best competitor in a tournament to the list
    return new_list
    
def get_average_fitness(puzzle_list):
    total_score = 0 #Set the total score to 0
    for cur_puzzle in puzzle_list: #For every puzzle
        total_score += cur_puzzle.get_fitness() #Add its fitness
    return (total_score/len(puzzle_list)) #Return the total fitness/number of puzzles
    
def mutate_list(puzzle_list, average_fitness):
    mutate_chance = 1/len(puzzle_list) #For a mutation chance of 1/population size
    for puzzle in puzzle_list: #For every puzzle in the list
        if(random() < mutate_chance): #and puzzle.get_fitness() < average_fitness): #Generate a random number, if it is less than the mutate chance
            mutate(puzzle, (1)) #Mutate the given puzzle
   
def begin_evolution(count, string_list, iteration_limit = 1000):
    population = populate(count, string_list) #Initialise the population
    highest_average_fitness = 0
    starting_average_fitness = get_average_fitness(population)
    best_puzzle = population[0] #Set the best puzzle as the first member of the population
    iteration = 0
    while (check_for_success(population) == None and iteration_limit > iteration): #Check for a condition
        population = get_next_generation(population) #Get the next generation
        average_fitness = get_average_fitness(population) #Get the fitness of the current generation
        mutate_list(population, average_fitness) #Mutate the next generation
        print("Pop fitness:", get_average_fitness(population)) #Print the current pop fitness
        if(get_average_fitness(population) > highest_average_fitness): #If there is a better average fitness
            highest_average_fitness = get_average_fitness(population) #Mark its value
        best_current_puzzle = deepcopy(get_best_puzzle(population)) #Get the best puzzle in the current population
        if (best_current_puzzle.get_fitness() > best_puzzle.get_fitness()): #If it is better than the previous best
            best_puzzle = best_current_puzzle #Copy it
        iteration += 1
    print("After", iteration,
          "iterations, the final average fitness was:", get_average_fitness(population),
          "\nThe highest average fitness was:", highest_average_fitness,
          "\nThe starting average fitness was:", starting_average_fitness)
    print("The best puzzle had a score of:", best_puzzle.get_fitness(),
          "and had the layout:")
    best_puzzle.print_puzzle()

def check_for_success(puzzle_list):
    for puzzle in puzzle_list: #For every puzzle
        if (puzzle.get_fitness() == 81): #Check it has a fitness of 81
            return puzzle #Return the puzzle if its fitness is 81
    return None #Otherwise, return nothing
    
def get_best_puzzle(puzzle_list):
    best_score = 0
    for puzzle in puzzle_list:
        if(puzzle.get_fitness() > best_score):
            best_puzzle = puzzle
    return best_puzzle

string_one = ["3..!..5!.47", "..6!.42!..1", "...!..7!89.", 
                ".5.!.16!..2", "..3!...!..4", "81.!...!7..",
                "..2!...!4..", "56.!87.!1..", "...!3..!6.."]
string_two = ["..2!...!634", "1.6!...!58.", "..7!3..!29.", 
                ".85!..1!..6", "...!75.!.23", "..3!...!.5.",
                "314!..2!...", "..9!.8.!4..", "72.!.4.!..9"]
string_three = ["..4!.1.!.6.", "9..!...!.3.", ".5.!796!...", 
                "..2!5.4!9..", ".83!.6.!...", "...!...!6.7",
                "...!9.3!.7.", "...!...!...", "..6!...!.1."]
string_list = [string_one, string_two, string_three]
input_seed = int(input("Please input the seed you would like to use for the random number generator:"))
seed(input_seed)
input_number = int(input("Please input the population number you would like to simulate:"))
input_index = int(input("Please input the puzzle number (1-3) you would like to simulate:"))
input_string = string_list[input_index - 1]
input_iterations = int(input("Please input the number of iterations you would like to simulate:"))
begin_evolution(input_number, input_string, input_iterations)