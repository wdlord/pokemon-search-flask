import requests
import random
import json
import unittest
from typing import Optional


# This loads a list of Pokémon names to be used with the 'random' button.
with open('pokemon_names.json', 'r') as f:
    pokemon_names = json.load(f)


def get_sprite(pokemon: dict) -> str:
    """
    Tries to get the animated sprite for a Pokémon if available, otherwise gets the default static sprite.
    Extension is .gif if animated, .png if static.
    """

    # The animated sprite can be None, so this statement will return the default sprite in that case.
    sprite_url = (
        pokemon['sprites']['versions']['generation-v']['black-white']['animated']['front_default']
        or
        pokemon['sprites']['front_default']
    )

    return sprite_url


def get_pokemon(name: Optional[str] = None) -> Optional[dict]:
    """
    Get a Pokémon by name, or a random Pokémon if no argument is passed.

    :param name: Case-insensitive Pokémon name (or None).
    :return: Pokémon dict from https://pokeapi.co
    """

    # Randomly select a Pokémon if no name is supplied.
    if not name:
        name = pokemon_names[random.randrange(0, len(pokemon_names))]
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name.lower()}/")

        if response.status_code == 404:
            return get_pokemon()

        elif response.status_code != 200:
            print(f"pokeapi error: {response.status_code}")

        pokemon = response.json()
        pokemon['sprite'] = get_sprite(pokemon)  # We add the sprite for easier access later.
        return pokemon

    # Attempt lookup if a name was supplied.
    else:
        name = name.lower().strip()
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{name}/")

        if response.status_code != 200:
            print(f"pokeapi error: {response.status_code}: {name}")
            return None

        pokemon = response.json()
        pokemon['sprite'] = get_sprite(pokemon)  # We add the sprite for easier access later.
        return pokemon


class TestInputs(unittest.TestCase):
    """
    This class contains unit tests for the get_pokemon() function.
    """

    def test_mixed_case(self):
        self.assertEqual(get_pokemon('pIKACHU')['name'], 'pikachu')

    def test_whitespace(self):
        self.assertEqual(get_pokemon('\tpikachu ')['name'], 'pikachu')

    def test_invalid_name(self):
        self.assertEqual(get_pokemon('Kuriboh'), None)

    def test_random(self):
        self.assertNotEqual(get_pokemon(), None)

    def test_show_expected_output(self):
        import json

        pokemon = get_pokemon('pikachu')
        print(json.dumps(pokemon, indent=4))

        self.assertEqual(pokemon['name'], 'pikachu')


if __name__ == "__main__":
    unittest.main()
