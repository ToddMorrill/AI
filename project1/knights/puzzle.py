from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
standard_specs = And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)))
knowledge0 = And(standard_specs, Or(And(AKnight, AKnave), AKnave))

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
standard_specs = And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)),
                     Or(BKnight, BKnave), Not(And(BKnight, BKnave)))
knowledge1 = And(standard_specs, Or(And(AKnave, BKnave), AKnave),
                 Not(And(And(AKnave, BKnave), AKnave)))

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
standard_specs = And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)),
                     Or(BKnight, BKnave), Not(And(BKnight, BKnave)))
knowledge2 = And(
    standard_specs,
    Or(And(AKnight, BKnight), And(AKnave, BKnight)),  # is this valid?
    # Not(And(And(AKnight, BKnight), And(AKnave, BKnight))),
    Or(And(BKnight, AKnave), BKnave),
    # Not(And(And(BKnight, AKnave), BKnave))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
standard_specs = And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)),
                     Or(BKnight, BKnave), Not(And(BKnight, BKnave)),
                     Or(CKnight, CKnave), Not(And(CKnight, CKnave)))
knowledge3 = And(
    standard_specs,
    Or(AKnight, AKnave),  # already captured in standard specs
    # the claim 'I am a Knave' is not possible
    Not(And(AKnight, AKnave)),  # already captured in standard specs
    BKnave,  # A didn't say 'I am a knave' - not possible
    Not(And(AKnave, BKnave)),
    Or(CKnave, BKnave),
    Not(And(CKnave, BKnave)),
    Or(And(AKnight, CKnight), CKnave),
    Not(And(And(AKnight, CKnight), CKnave)))


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [("Puzzle 0", knowledge0), ("Puzzle 1", knowledge1),
               ("Puzzle 2", knowledge2), ("Puzzle 3", knowledge3)]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
