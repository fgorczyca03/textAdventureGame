import unittest

from game import TextAdventureGame


class TestTextAdventureGame(unittest.TestCase):
    def run_path(self, game: TextAdventureGame, commands: list[str]) -> str:
        result = ""
        for command in commands:
            result = game.process_command(command)
        return result

    def test_ruins_puzzle_unlocks_archive_and_reward(self):
        game = TextAdventureGame()
        game.process_command("go east")
        blocked = game.process_command("go east")
        self.assertIn("puzzle", blocked.lower())

        solved = game.process_command("solve echo")
        self.assertIn("Correct", solved)
        self.assertIn("crystal shard", game.state.inventory)

        moved = game.process_command("go east")
        self.assertIn("Archive Hall", moved)

    def test_marsh_and_cave_require_items(self):
        game = TextAdventureGame()

        game.process_command("go west")
        marsh_block = game.process_command("go west")
        self.assertIn("brass key", marsh_block)

        self.run_path(
            game,
            [
                "go east",
                "go north",
                "go northeast",
                "take brass key",
                "go southwest",
                "go south",
                "go south",
                "go east",
                "take lantern oil",
                "go west",
                "go north",
                "go west",
                "go west",
                "go west",
            ],
        )
        self.assertEqual(game.state.current_room, "Deep Grotto")

    def test_status_and_lore_commands(self):
        game = TextAdventureGame()
        self.assertIn("Elders", game.process_command("lore"))
        status = game.process_command("status")
        self.assertIn("Puzzles solved", status)

    def test_full_winning_route(self):
        game = TextAdventureGame()

        result = self.run_path(
            game,
            [
                # Gather utility items.
                "go south",
                "go east",
                "take lantern oil",
                "go west",
                "go north",
                "go north",
                "go northeast",
                "take brass key",
                "go southwest",
                # Observatory puzzle.
                "go northwest",
                "go up",
                "solve sun",
                "go down",
                "go southeast",
                # Ruins puzzle + archive relic.
                "go south",
                "go east",
                "solve echo",
                "go east",
                "take silver compass",
                # Cave relic.
                "go west",
                "go west",
                "go west",
                "go west",
                "go west",
                "take sun gem",
                # Final sanctum.
                "go north",
                "go north",
            ],
        )

        self.assertIn("You win", result)
        self.assertTrue(game.state.flags["won"])


if __name__ == "__main__":
    unittest.main()
