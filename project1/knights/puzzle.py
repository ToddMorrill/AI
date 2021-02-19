from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
standard_specs = Biconditional(AKnight, Not(AKnave))
knowledge0 = And(
    standard_specs,
    # AKnave iff (AKnave and AKnight)
    Biconditional(AKnave, And(AKnight, AKnave)))

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
standard_specs = And(Biconditional(AKnight, Not(AKnave)),
                     Biconditional(BKnight, Not(BKnave)))
knowledge1 = And(
    standard_specs,
    # AKnight iff (AKnave and BKnave)
    Biconditional(AKnight, And(AKnave, BKnave)))

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
standard_specs = And(Biconditional(AKnight, Not(AKnave)),
                     Biconditional(BKnight, Not(BKnave)))
knowledge2 = And(
    standard_specs,
    # AKnight iff (AKnight and BKnight)
    Biconditional(AKnight, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    # BKnight iff (BKnight and AKnave)
    Biconditional(BKnight, Or(And(BKnight, AKnave), And(BKnave, AKnight))))

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
standard_specs = And(Biconditional(AKnight, Not(AKnave)),
                     Biconditional(BKnight, Not(BKnave)),
                     Biconditional(CKnight, Not(CKnave)))
knowledge3 = And(
    standard_specs,
    # (AKnight iff AKnight) or (AKnight iff AKnave)
    Or(Biconditional(AKnight, AKnight), Biconditional(AKnight, AKnave)),
    # BKnight iff (AKnight iff AKnave)
    Biconditional(BKnight, Biconditional(AKnight, AKnave)),
    # BKnight iff CKnave
    Biconditional(BKnight, CKnave),
    # CKnight iff AKnight
    Biconditional(CKnight, AKnight))


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
