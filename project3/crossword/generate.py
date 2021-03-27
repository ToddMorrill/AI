"""
This module implements the crossword solver using a backtrack search procedure.

Examples:
    $ python3 generate.py data/structure0.txt data/words0.txt output0.png
    $ python3 generate.py data/structure1.txt data/words1.txt output1.png
    $ python3 generate.py data/structure2.txt data/words2.txt output2.png
"""
import copy
import itertools
import sys

from crossword import *


class CrosswordCreator():
    def __init__(self, crossword: Crossword) -> None:
        """Create new CSP crossword generate.

        Args:
            crossword (Crossword): Crossword problem instance.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment: dict) -> list:
        """Return 2D array representing a given assignment.

        Args:
            assignment (dict): Dictionary assigning variables to words.

        Returns:
            list: Filled in crossword in list form.
        """
        letters = [[None for _ in range(self.crossword.width)]
                   for _ in range(self.crossword.height)]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment: dict) -> None:
        """Print crossword assignment to the terminal.

        Args:
            assignment (dict): Dictionary assigning variables to words.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment: dict, filename: str) -> None:
        """Save crossword assignment to an image file.

        Args:
            assignment (dict): Dictionary assigning variables to words.
            filename (str): File where image will be saved.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new("RGBA", (self.crossword.width * cell_size,
                                 self.crossword.height * cell_size), "black")
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [(j * cell_size + cell_border,
                         i * cell_size + cell_border),
                        ((j + 1) * cell_size - cell_border,
                         (i + 1) * cell_size - cell_border)]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j],
                            fill="black",
                            font=font)

        img.save(filename)

    def solve(self) -> dict:
        """Enforce node and arc consistency, and then solve the CSP.

        Returns:
            dict: Assignment dictionary if found, else None.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self) -> None:
        """Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.domains:
            for word in list(self.domains[var]):
                if len(word) != var.length:
                    self.domains[var].remove(word)

    def revise(self, x: Variable, y: Variable) -> bool:
        """Make variable `x` arc consistent with variable `y`. To do so, remove
         values from `self.domains[x]` for which there is no possible
         corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return False
         if no revision was made.

        Args:
            x (Variable): Variable whose domain is being reduced.
            y (Variable): Variable whose domain x's domain is being compared
             to.

        Returns:
            bool: True if revised, otherwise False.
        """
        revised = False
        overlap = self.crossword.overlaps[x, y]
        if overlap:
            # where x's ith character overlaps y's jth character
            i, j = overlap
            # remove any inconsistent values in x's domain
            for x_word in list(self.domains[x]):
                characters_agree = False
                # check if y has any words that meet the constraints
                for y_word in self.domains[y]:
                    if x_word[i] == y_word[j]:
                        # y has a word that meets the contstraint
                        # keep word and move on to next word
                        characters_agree = True
                        break
                if not characters_agree:
                    self.domains[x].remove(x_word)
                    revised = True
        return revised

    def ac3(self, arcs: list = None) -> bool:
        """Update `self.domains` such that each variable is arc consistent. If
         `arcs` is None, begin with initial list of all arcs in the problem.
         Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
         return False if one or more domains end up empty.

        Args:
            arcs (list, optional): Optional list of pairs of variables to make
                 arc consistent. Defaults to None.

        Returns:
            bool: True if revised, otherwise False.
        """
        if not arcs:
            arcs = []
            # generate list of all arcs in the problem (i.e. all the pairs of
            # nodes that overlap)
            for x in self.domains:
                for y in self.domains:
                    if x == y:
                        continue
                    if self.crossword.overlaps[x, y]:
                        arcs.append((x, y))

        for arc in arcs:
            x, y = arc
            if self.revise(x, y):
                # x no longer has any elements in its domain, unsatisfiable
                if len(self.domains[x]) == 0:
                    return False

                # may have dispruted neighbors
                for z in self.domains:
                    # avoid adding to the queue twice
                    if (z == y) or (z == x):
                        continue
                    if self.crossword.overlaps[x, z]:
                        arcs.append((z, x))

        return True

    def assignment_complete(self, assignment: dict) -> bool:
        """Return True if `assignment` is complete (i.e., assigns a value to
         each crossword variable); return False otherwise.

        Args:
            assignment (dict): Dictionary assigning variables to words.

        Returns:
            bool: True if assignment complete, otherwise False.
        """
        for var in self.domains:
            # check if var in assignment
            if var not in assignment:
                return False

            # if the val is not a string or if it's an empty string, incomplete
            if not isinstance(assignment[var], str) or (len(assignment[var])
                                                        == 0):
                return False
        return True

    def consistent(self, assignment: dict) -> bool:
        """Return True if `assignment` is consistent (i.e., words fit in
         crossword puzzle without conflicting characters); return False
         otherwise.

        Args:
            assignment (dict): Dictionary assigning variables to words.

        Returns:
            bool: True if consistent, otherwise False.
        """
        # an assignment is consistent if it satisfies:
        # all values are distinct
        if len(set(assignment.values())) != len(assignment):
            return False

        # every value is the correct length
        for var in assignment:
            if var.length != len(assignment[var]):
                return False

        # no conflicts between neighboring variables
        for x_var, y_var in itertools.combinations(assignment.keys(), 2):
            overlap = self.crossword.overlaps[x_var, y_var]
            if overlap:
                i, j = overlap
                if assignment[x_var][i] != assignment[y_var][j]:
                    return False

        return True

    def order_domain_values(self, var: Variable, assignment: dict) -> list:
        """Return a list of values in the domain of `var`, in order by the
         number of values they rule out for neighboring variables. The first
         value in the list, for example, should be the one that rules out the
         fewest values among the neighbors of `var`.

        Args:
            var (Variable): Variable whose domain should be ordered.
            assignment (dict): Dictionary assigning variables to words.

        Returns:
            list: Ordered list of values from the variable's domain.
        """
        # compute neighbors
        neighbors = self.crossword.neighbors(var)

        domain_scores = []
        for var_word in self.domains[var]:
            conflicts = 0
            for neighbor in neighbors:
                # don't count neighbors that have assignments
                if neighbor in assignment:
                    continue
                i, j = self.crossword.overlaps[var, neighbor]
                # loop through domain of neighbor_var and count how many
                # conflicts occur
                for neighbor_word in self.domains[neighbor]:
                    if var_word[i] != neighbor_word[j]:
                        conflicts += 1
            domain_scores.append((var_word, conflicts))

        domain_scores.sort(key=lambda x: x[1])
        words, scores = zip(*domain_scores)
        return list(words)

    def select_unassigned_variable(self, assignment: dict) -> Variable:
        """Return an unassigned variable not already part of `assignment`.
         Choose the variable with the minimum number of remaining values in its
         domain. If there is a tie, choose the variable with the highest
         degree. If there is a tie, any of the tied variables are acceptable
         return values.

        Args:
            assignment (dict): Dictionary assigning variables to words.

        Returns:
            Variable: Variable to assign value to next.
        """
        unassigned_vars = []
        for var in self.domains:
            if var not in assignment:
                unassigned_vars.append(var)

        var_scores = []
        for var in unassigned_vars:
            num_remaining_vals = len(self.domains[var])
            num_neighbors = len(self.crossword.neighbors(var))
            var_scores.append((var, num_remaining_vals, num_neighbors))

        var_scores.sort(key=lambda x: (x[1], -x[2]))
        vars, remaining_vals, degrees = zip(*var_scores)
        return vars[0]

    def backtrack(self, assignment: dict) -> dict:
        """Using Backtracking Search, take as input a partial assignment for
         the crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.

        Args:
            assignment (dict): Dictionary assigning variables to words.

        Returns:
            dict: Complete assignment of words to all the variables.
        """
        # base case
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for word in self.order_domain_values(var, assignment):
            # make a copy of assignment so we can revert back if attempt fails
            assignment_attempt = assignment.copy()
            assignment_attempt[var] = word
            if self.consistent(assignment_attempt):
                # maintain arc consistency for arcs impacted
                neighbors = self.crossword.neighbors(var)
                arcs_impacted = []
                for neighbor in neighbors:
                    if neighbor not in assignment_attempt:
                        arcs_impacted.append((neighbor, var))

                # need to make a copy of self and update the domain according
                # to the assignment to var in order for ac3 to work
                # need to make a copy so we don't commit to this assignment
                self_copy = copy.deepcopy(self)
                self_copy.domains[var] = {word}

                # run ac3 to maintain arc consistency
                if self_copy.ac3(arcs_impacted):
                    # check if any domains are singletons that can be added to
                    # assignment
                    for x, y in arcs_impacted:
                        if len(self_copy.domains[x]) == 1:
                            # get the one and only element from the domain set
                            assignment_attempt[x] = list(
                                self_copy.domains[x])[0]
                    result = self_copy.backtrack(assignment_attempt)
                    if result:
                        return result
        return None


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
