import itertools
import random


class Minesweeper():
    """Minesweeper game representation."""
    def __init__(self, height=8, width=8, mines=8):
        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """Prints a text-based representation of where mines are located."""
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """Returns the number of mines that are within one row and column of a 
        given cell, not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """Checks if all mines have been flagged."""
        return self.mines_found == self.mines


class Sentence():
    """A logical statement about a Minesweeper game.

    A sentence consists of a set of board cells, and a count of the number of 
    those cells which are mines.
    """
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def not_empty(self) -> bool:
        """Checks if a sentence is not empty

        Returns:
            bool: True if not empty, False otherwise.
        """
        return (self.cells != set()) and (self.count != 0)

    def known_mines(self) -> set:
        """Returns the set of all cells in self.cells known to be mines.

        Returns:
            set: Set of cells.
        """
        # inference rule 1
        if len(self.cells) == self.count:
            return self.cells
        return set()

    def known_safes(self) -> set:
        """Returns the set of all cells in self.cells known to be safe.

        Returns:
            set: Set of cells.
        """
        # inference rule 2
        if self.count == 0:
            return self.cells
        return set()

    def mark_mine(self, cell: tuple) -> None:
        """Updates internal knowledge representation given the fact that a cell 
        is known to be a mine.

        Args:
            cell (tuple): Row and column index.
        """
        if cell in self.cells:
            # remove cell and decrement counter
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell: tuple) -> None:
        """Updates internal knowledge representation given the fact that a cell 
        is known to be safe.

        Args:
            cell (tuple): Row and column index.
        """
        if cell in self.cells:
            # remove cell, don't decrement counter
            self.cells.remove(cell)


class MinesweeperAI():
    """An AI-based minesweeper game player."""
    def __init__(self, height=8, width=8):
        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell: tuple) -> None:
        """Marks a cell as a mine, and updates all knowledge to mark that cell 
        as a mine as well.

        Args:
            cell (tuple): Row and column index.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell: tuple) -> None:
        """Marks a cell as safe, and updates all knowledge to mark that cell as 
        safe as well.

        Args:
            cell (tuple): Row and column index.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def get_unknown_neighbors(self, cell: tuple) -> tuple:
        """Retrieve unknown neighbors within one row and column of the passed 
        cell. Unknown neighbors are not flagged as mines or safes. Count mines 
        among neighbors.

        Args:
            cell (tuple): Row and column index.

        Returns:
            tuple: Set of unknown neighbors and mine counts.
        """
        unknowns = set()
        mine_count = 0
        # loop over all cells within one row and column
        one_row = range(cell[0] - 1, cell[0] + 2)
        one_col = range(cell[1] - 1, cell[1] + 2)
        for i, j in itertools.product(one_row, one_col):
            # ignore self and cells off board
            current_cell = (i, j) == cell
            off_row = (i < 0) or (i >= self.height)
            off_col = (j < 0) or (j >= self.width)
            if current_cell or off_row or off_col:
                continue
            # if cell unknown, add it to the set
            if ((i, j) not in self.mines) and ((i, j) not in self.safes):
                unknowns.add((i, j))
            # if cell is a mine, increment counter
            if (i, j) in self.mines:
                mine_count += 1
        return unknowns, mine_count

    def mark_cells(self, known_mines: set, known_safes: set) -> None:
        """Mark all cells in a set as mines or safes. known_mines and 
        known_safes are mutually exclusive - if one is not empty the other is 
        empty.

        Args:
            known_mines (set): Set of known mine cells.
            known_safes (set): Set of known safe cells.
        """
        # update mines, sentences, and drop sentence from KB
        if known_mines:
            # list prevents error about changes to the set while iterating
            for cell in list(known_mines):
                self.mark_mine(cell)
        # update safes, sentences, and drop sentence from KB
        elif known_safes:
            # list prevents error about changes to the set while iterating
            for cell in list(known_safes):
                self.mark_safe(cell)

    def _mark_mines_safes(self) -> bool:
        """Uses two basic inference rules encoded in sentence.mines() and 
        sentence.safes() to determine if a sentence consists of mines or safes
        and marks them accordingly. 

        Returns:
            bool: True if inferences made, False otherwise.
        """
        changes = False
        new_knowledge = []
        for sentence in self.knowledge:
            known_mines = sentence.known_mines()
            known_safes = sentence.known_safes()
            # update mines/safes, sentences
            if known_mines or known_safes:
                self.mark_cells(known_mines, known_safes)
                changes = True
            # no conclusion drawn, keep sentence
            else:
                new_knowledge.append(sentence)

        # update knowledge, remove duplicates and empty sentences
        self.knowledge = []
        for sentence in new_knowledge:
            if sentence.not_empty() and (sentence not in self.knowledge):
                self.knowledge.append(sentence)
        return changes

    def mark_mines_safes(self) -> None:
        """Iteratively mark mines and safes in the sentences in self.knowledge 
        until no changes are detected.
        """
        changes = True
        while changes:
            changes = self._mark_mines_safes()

    def _infer_new_sentences(self) -> bool:
        """Use the subset inference rule to create new sentences to be added to
        self.knowledge.

        Returns:
            bool: True if new sentences created, False otherwise.
        """
        changes = False
        new_knowledge = []
        for sentence1, sentence2 in itertools.permutations(self.knowledge, 2):
            if sentence1.cells.issubset(sentence2.cells):
                difference = sentence2.cells.difference(sentence1.cells)
                count = sentence2.count - sentence1.count
                new_sentence = Sentence(difference, count)
                # if not in new_knowledge and not in existing knowledge
                net_new = (new_sentence not in new_knowledge)
                net_new = net_new and (new_sentence not in self.knowledge)
                if net_new:
                    new_knowledge.append(new_sentence)
                    changes = True

        self.knowledge += new_knowledge

        if changes:
            # clean up the KB
            self.mark_mines_safes()

        return changes

    def infer_new_sentences(self) -> None:
        """Iteratively infer new sentences until no new changes are detected.
        """
        changes = True
        # iteratively update until the knowledge stops changing
        while changes:
            changes = self._infer_new_sentences()

    def add_knowledge(self, cell: tuple, count: int) -> None:
        """Called when the Minesweeper board tells us, for a given safe cell, 
        how many neighboring cells have mines in them.

        This function:
            1) marks the cell as a move that has been made
            2) marks the cell as safe
            3) adds a new sentence to the AI's knowledge base based on the value
               of `cell` and `count`
            4) marks any additional cells as safes or as mines if it can be 
               concluded based on the AI's knowledge base
            5) adds any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        
        Args:
            cell (tuple): Row and column index.
            count (int): Number of neighboring cells containing mines.
        """
        # mark cell as a move
        self.moves_made.add(cell)

        # mark the cell as safe, update sentences
        self.mark_safe(cell)

        # get unknown neighbors
        unknown_neighbors, mine_count = self.get_unknown_neighbors(cell)
        # add new sentence to KB
        if unknown_neighbors:
            # subtract known mines from the count
            self.knowledge.append(
                Sentence(unknown_neighbors, count - mine_count))

        # mark any known safes or mines
        self.mark_mines_safes()

        # infer new sentences
        self.infer_new_sentences()

    def make_safe_move(self) -> tuple:
        """Returns a safe cell to choose on the Minesweeper board. The move must
         be known to be safe, and not already a move that has been made.

        This function may use the knowledge in self.mines, self.safes and 
        self.moves_made, but should not modify any of those values.

        Returns:
            tuple: Row and column index of move.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self, first_available: bool = False) -> tuple:
        """Returns a move to make on the Minesweeper board. Should choose 
        randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines

        Args:
            first_available (bool, optional): If True, upper-leftmost cell 
            available, otherwise random among remaining options. Defaults to 
            True.

        Returns:
            tuple: Row and column index
        """
        moves_remaining = []
        for i, j in itertools.product(range(self.height), range(self.width)):
            if ((i, j) not in self.moves_made) and ((i, j) not in self.mines):
                if first_available:
                    return (i, j)
                moves_remaining.append((i, j))

        if moves_remaining:
            return random.choice(moves_remaining)
        return None
