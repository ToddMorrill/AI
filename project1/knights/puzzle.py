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
knowledge0 = And(
    standard_specs,
    # both knight/knave (spoiler: it's a lie) or A is a lying knave
    Or(And(AKnight, AKnave), AKnave))

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
standard_specs = And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)),
                     Or(BKnight, BKnave), Not(And(BKnight, BKnave)))
knowledge1 = And(
    standard_specs,
    # both knaves (spoiler: not possible)) or A is a lying knave
    Or(And(AKnave, BKnave), AKnave),
    Not(And(And(AKnave, BKnave), AKnave)))  # can't be both

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
standard_specs = And(Or(AKnight, AKnave), Not(And(AKnight, AKnave)),
                     Or(BKnight, BKnave), Not(And(BKnight, BKnave)))
knowledge2 = And(
    standard_specs,
    # either both knights, or A is a lying Knave
    Or(And(AKnight, BKnight), AKnave),
    # if A is a lying Knave, then they are not the same kind (i.e. BKnight)
    Implication(AKnave, BKnight),
    # either different (and B is an honest Knight) or B is a lying Knave
    Or(And(BKnight, AKnave), BKnave))

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
    # the claim 'I am a Knave' -> I lie -> I am a Knight -> I tell the truth (contradiction, wasn't said)
    # from which we conclude A said 'I am a Knight', so A is an honest Knight or lying Knave
    # Or(AKnight, AKnave) already captured in standard specs
    # If A said 'I am a knight' (didn't say 'I am a knave') then B is a lying knave
    Implication(Or(AKnight, AKnave), BKnave),
    # Either C is a knave (and B is an honest knight) or B is a lying knave and C is a knight
    Or(And(CKnave, BKnight), And(BKnave, CKnight)),
    # Either C is an honest knight and AKnight or C is a lying knave and A is a knave
    Or(And(AKnight, CKnight), And(CKnave, AKnave)))


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
