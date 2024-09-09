import os
import random

pokemon_dict = {

}


def populate_pokemon_dict():

    # Get the current directory
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Define the directory name
    pokemon_directory = os.path.join(current_directory, 'pokemon')

    # Get all file paths in the pokemon directory
    file_paths = [os.path.join(pokemon_directory, file) for file in os.listdir(pokemon_directory)]

    # Get only the file names from the file paths and remove the ".png" extension
    file_names = [os.path.splitext(os.path.basename(file_path))[0] for file_path in file_paths]

    r = 0
    for i in file_paths:
        pokemon_dict[r] = {"name": file_names[r], "path": i, "rank": random.randint(50, 10000)}
        r += 1

    return pokemon_dict

dc = populate_pokemon_dict()
print(dc)