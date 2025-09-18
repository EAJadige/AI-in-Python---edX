import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)         
        """
        # self.domain = dict {variable v : set(words x)}
        # Remove words which has not the same number of characters than the lenght of the variable
        for v in list(self.domains.keys()):
            for x in self.domains[v].copy():
                if not len(x) == v.length:
                    self.domains[v].remove(x)
        
        return 0
        raise NotImplementedError

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        revise = False
        remove = True        
        #Find overlap between variables x and y
        overlap = self.crossword.overlaps[x, y]
        if overlap is None:
            return revise
        else:
            #The characters must match according to the result of the overlap
            for word_x in list(self.domains[x]):
                for word_y in list(self.domains[y]):
                    if word_x[overlap[0]] == word_y[overlap[1]]:
                        #If the algorithm find a value in Y's domain, do not remove word in X's domain 
                        remove = False
                        break
                        
                
                if remove:
                    self.domains[x].remove(word_x)
                    revise = True
                else:
                    remove = True
                            
                        
            return revise
                                
        raise NotImplementedError

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        queue = list()
        arc = tuple()
        
        if arcs == None:
            #Initial list of arcs in the problem            
            #Create every combination of existing variables
            for v1 in self.crossword.variables:
                for v2 in self.crossword.variables:
                    if not v1 == v2:
                        #Create a tuple of two different variables
                        queue.append((v1,v2))
            
        else:
            queue = arcs
            
        #Run AC3 algorithm
        while len(queue) > 0:
            #Dequeue an arc and check arc-consistency
            arc = queue[0]
            queue.pop(0)
            if self.revise(arc[0], arc[1]):
                #Check if the domain is empty and there is no solution
                if len(self.domains[arc[0]]) == 0:
                    return False
                #Add new arcs to check if still arc consistency
                check_neighbors = self.crossword.neighbors(arc[0])
                check_neighbors.remove(arc[1])
                for z in check_neighbors:
                    #Enqueue new arc
                    queue.append((z,arc[0]))
                                
        return True                                         
        
        raise NotImplementedError

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        
        #assignment = dict (variable: word)                
        
        if len(assignment) == 0:
            return False
        else:
            for v in self.crossword.variables:
                if not v in assignment:
                    return False
            
        return True
        
        raise NotImplementedError

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        #Check if all values are distinct
        values = list(assignment.values())
        for v in values:
            if values.count(v) > 1:
                return False
                
        #Check if every value is the correct lenght and possible conflicts with neighbors
        for v in self.crossword.variables:
            word_lenght = v.length
            if v in assignment:
                string_lenght = len(assignment[v])
                if not word_lenght == string_lenght:
                    return False
            
            #Possible conflicts with neighbors
            for n in self.crossword.neighbors(v):
                overlap = self.crossword.overlaps[v, n]
                if overlap is not None:
                    #Check if each word overlapping has the same character
                    if (v in assignment) and (n in assignment):
                        if not assignment[v][overlap[0]] == assignment[n][overlap[1]]:
                            return False
            
        return True
        raise NotImplementedError

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        domain = list()
        
        #Fill the list with the var's domain
        for w in self.domains[var]:
            domain.append(w)
            
        #Define the function to determine the sort criteria
        def number_values(word):
            number = 0
            unassigned_neighbors = list()
            
            #Add to the list unassigned neighbors variables
            for n in self.crossword.neighbors(var):
                
                if not n in assignment:
                    unassigned_neighbors.append(n) 
            
            #Count the number of times that the var's word appears in neighbors domain        
            for x in unassigned_neighbors:
                if word in self.domains[x]:
                    number = number + 1
                
            return number
        
        domain.sort(reverse=False, key=number_values) 
        return domain       
        
        raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned_v = list()
        for v in self.crossword.variables:
            #Search for an unassigned variable and append to the list
            if not v in list(assignment.keys()):
                unassigned_v.append(v)
        
        min_domain = len (self.crossword.words)             
        for v in unassigned_v:
            #Search for the minimum number of words in a variable's domain
            if len(self.domains[v]) < min_domain:
                min_domain = len(self.domains[v])
                
        #Delete the variables which don't match the number of variables in its domain
        for v in unassigned_v.copy():
            if len(self.domains[v]) > min_domain:
                unassigned_v.remove(v)
                
        #Search for the highest degree variable
        hdegree_variable = 0        
        
        result = Variable(0, 0, 'down', 0)
        
        for v in unassigned_v:
            if len(self.crossword.neighbors(v)) > hdegree_variable:
                result = v
                hdegree_variable = len(self.crossword.neighbors(v))
                
        return result        
        
        raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        partial_assignment = assignment
        #Return when assignment is complete
        if self.assignment_complete(partial_assignment):
            return partial_assignment
        #Select an unassigned variable
        var = self.select_unassigned_variable(partial_assignment)
        list_values = self.order_domain_values(var, partial_assignment)
        for value in list_values:
            if self.consistent(partial_assignment):
                #New assignment
                partial_assignment[var] = value
                result = self.backtrack(partial_assignment)
                if result is not None:
                    return partial_assignment
                #If there is an error in assignment, remove the value
                partial_assignment.pop(var)
            
        return None
        
        raise NotImplementedError


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
