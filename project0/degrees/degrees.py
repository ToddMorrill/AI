import csv
import sys

from util import Node, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory: str) -> None:
    """Load data from CSV files into memory.

    Args:
        directory (str): Directory where data is stored.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def person_id_for_name(name: str) -> int:
    """Returns the IMDB id for a person's name, resolving ambiguities as needed.

    Args:
        name (str): Person's name.

    Returns:
        int: Person's ID.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id: int) -> set:
    """Returns (movie_id, person_id) pairs for people who starred with a given 
    person.

    Args:
        person_id (int): Person ID.

    Returns:
        set: Set of neighbors.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


def get_path(node: Node) -> list:
    """Utility function to follow the linked list back to the source node.

    Args:
        node (Node): The node to start traversing from.

    Returns:
        list: List of (movie_id, person_id) pairs along the path back to the 
        source node.
    """
    # handle case where the node is the source and the target
    if node.parent is None:
        # return length 0 list per problem specification
        return []
    path = []
    while node.parent != None:
        path.append((node.action, node.state))
        node = node.parent
    path.reverse()
    return path


def shortest_path(source: int, target: int) -> list:
    """ Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.

    Args:
        source (int): Source state.
        target (int): Target state.

    Returns:
        list: List of (movie_id, person_id) pairs along the path back to the 
        source node.
    """
    node = Node(source, None, None)
    # return path if the node is the target node (case when source == target)
    if node.state == target:
        return get_path(node)
    # add the source node to the frontier
    frontier = QueueFrontier()
    frontier.add(node)
    visited = set()

    # while the frontier isn't empty
    while not frontier.empty():
        node = frontier.remove()
        visited.add(node.state)
        neighbors = neighbors_for_person(node.state)
        for neighbor in neighbors:
            # expand the node if not already visited and not in frontier
            if (neighbor[1] not in visited) and (not frontier.contains_state(
                    neighbor[1])):
                # if node is goal state, return immediately (per hint)
                if neighbor[1] == target:
                    return get_path(Node(neighbor[1], node, neighbor[0]))
                # persist parent node and movie in action
                frontier.add(Node(neighbor[1], node, neighbor[0]))
    # queue is empty, no path found
    return None


def main(directory):
    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"
    main(directory)
