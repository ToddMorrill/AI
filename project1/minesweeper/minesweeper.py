import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """
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
        """
        Prints a text-based representation
        of where mines are located.
        """
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
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
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
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # if len(self.cells) == self.count == 0:
        #     breakpoint()
        if len(self.cells) == self.count:
            # print(self.__str__())
            # breakpoint()
            return self.cells
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            # remove cell and decrement counter
            self.cells.remove(cell)
            # if self.cells == set():
            #     breakpoint()
            self.count -= 1  # any concerns about going negative?
            if len(self.cells) < self.count:
                breakpoint()

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            # remove cell, don't decrement counter
            self.cells.remove(cell)
            # if self.cells == set():
            #     breakpoint()
            if len(self.cells) < self.count:
                # why would this happen?
                breakpoint()
            # make sure 


iteration_counter = 0


class MinesweeperAI():
    """
    Minesweeper game player
    """
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

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def get_unknown_neighbors(self, cell):
        unknowns = set()
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # if cell off board
                if (i < 0) or (i >= self.height) or (j < 0) or (j >=
                                                                self.width):
                    continue

                # if cell unknown, add it to the set
                # TODO: probably not necessary to check in moves_made 
                if ((i, j) not in self.mines) and (
                    (i, j) not in self.safes) and ((i, j)
                                                   not in self.moves_made):
                    unknowns.add((i, j))
        return unknowns

    def mark_mines_safes_delete_sentences(self):
        changes = False
        new_knowledge = []
        # will be modifying the items in self.knowledge
        knowledge_copy = self.knowledge
        for sentence in knowledge_copy:
            known_mines = sentence.known_mines()
            known_safes = sentence.known_safes()
            if known_safes and known_mines:
                breakpoint()
            if known_mines:
                # breakpoint()
                # update mines, sentences, and drop sentence from KB
                for cell in list(known_mines):
                    self.mark_mine(cell)
                changes = True
            elif known_safes:
                # update safes, sentences, and drop sentence from KB
                for cell in list(known_safes):
                    self.mark_safe(cell)
                changes = True
            if (sentence.cells == set()) and (sentence.count == 0):
                continue
            # if no conclusion drawn, keep sentence
            new_knowledge.append(sentence)
        # update knowledge
        self.knowledge = new_knowledge
        return changes

    def _infer_new_sentences(self):
        # breakpoint()
        # should this be implemented by depth first recursion?
        changes = False
        new_knowledge = []
        # need to deep copy this?
        # existing_knowledge = self.knowledge
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                # no need to compare to self
                if sentence1 == sentence2:
                    # TODO: find a better approach
                    if sentence1 not in new_knowledge:
                        new_knowledge.append(sentence1)
                    if sentence2 not in new_knowledge:
                        new_knowledge.append(sentence2)
                    continue
                elif sentence1.cells == sentence2.cells:
                    breakpoint()
                elif sentence1.cells.issubset(sentence2.cells):
                    difference = sentence2.cells.difference(sentence1.cells)
                    if sentence2.count < sentence1.count:
                        breakpoint()
                    count = sentence2.count - sentence1.count
                    if count > len(difference):
                        breakpoint()
                    new_sentence = Sentence(difference, count)
                    if new_sentence in self.knowledge:
                        breakpoint()
                        continue
                    new_knowledge.append(new_sentence)
                    if sentence1 not in new_knowledge:
                        new_knowledge.append(sentence1)
                    if sentence2 not in new_knowledge:
                        new_knowledge.append(sentence2)
                    changes = True
                    # self.knowledge.append(new_sentence)
                    # new_knowledge.append(new_sentence)
                    # remove old sentence, no longer needed
                    # self.knowledge.remove(sentence2)
        self.knowledge = new_knowledge

        # should we try to clean up the knowledge base here too?
        other_changes = self.mark_mines_safes_delete_sentences()

        return changes, other_changes

    def infer_new_sentences(self):
        infer_changes, delete_changes = True, True
        # iteratively update until the knowledge stops changing
        while infer_changes or delete_changes:
            infer_changes, delete_changes = self._infer_new_sentences()

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # breakpoint()
        # mark cell as a move
        self.moves_made.add(cell)

        # mark the cell as safe, update sentences
        self.mark_safe(cell)

        # add new sentence to knowledge base
        # get unknown neighbors
        unknown_neighbors = self.get_unknown_neighbors(cell)

        # add new sentence to KB
        if len(unknown_neighbors) > 0:
            # count should be the min(count, len(unknown_neighbors))
            revised_count = min(count, len(unknown_neighbors))
            # if revised_count == len(unknown_neighbors):
                # breakpoint()
            self.knowledge.append(Sentence(unknown_neighbors, revised_count))

        # check for any known safes or mines
        # delete sentences if possible
        self.mark_mines_safes_delete_sentences()

        # infer new sentences
        self.infer_new_sentences()
        # breakpoint()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        for i in range(self.height):
            for j in range(self.width):
                not_move_made = ((i, j) not in self.moves_made)
                not_mine = ((i, j) not in self.mines)
                if not_move_made and not_mine:
                    return (i, j)
        return None