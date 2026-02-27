#!/usr/bin/env python3
"""Echoes of the Valley - a console text adventure with branching routes, inventory, and puzzles."""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class Puzzle:
    puzzle_id: str
    prompt: str
    answers: Tuple[str, ...]
    reward: Optional[str] = None


@dataclass
class Room:
    name: str
    description: str
    exits: Dict[str, str]
    items: List[str] = field(default_factory=list)
    lore: Optional[str] = None
    puzzle: Optional[Puzzle] = None
    locked_exits: Dict[str, str] = field(default_factory=dict)


@dataclass
class GameState:
    current_room: str = "Crossroads"
    inventory: Set[str] = field(default_factory=set)
    solved_puzzles: Set[str] = field(default_factory=set)
    flags: Dict[str, bool] = field(default_factory=lambda: {"won": False, "lost": False})


class TextAdventureGame:
    def __init__(self) -> None:
        self.rooms = self._build_world()
        self.state = GameState()
        self.final_relics = {"crystal shard", "sun gem", "silver compass", "star sigil"}

    def _build_world(self) -> Dict[str, Room]:
        return {
            "Crossroads": Room(
                name="Crossroads",
                description=(
                    "You arrive at the Valley Crossroads where four old roads diverge. "
                    "A weather-worn marker points toward forest ruins, flooded marsh, and a sleeping village."
                ),
                exits={
                    "north": "Forest Trail",
                    "east": "Ruins Gate",
                    "west": "Marsh Path",
                    "south": "Village Square",
                },
                lore="Elders once said the valley seals itself unless four relics are reunited.",
            ),
            "Village Square": Room(
                name="Village Square",
                description=(
                    "Abandoned carts and shuttered homes surround an old well. "
                    "A tiny healer's hut still glows with a pale green lantern."
                ),
                exits={"north": "Crossroads", "east": "Healer Hut"},
                lore="The village fled after the sanctum lights went dark generations ago.",
            ),
            "Healer Hut": Room(
                name="Healer Hut",
                description=(
                    "Inside, dusty herbs hang from rafters. A sealed flask labeled 'Lantern Oil' sits by a note: "
                    "'For the caves where sunlight never reaches.'"
                ),
                exits={"west": "Village Square"},
                items=["lantern oil"],
            ),
            "Forest Trail": Room(
                name="Forest Trail",
                description=(
                    "A winding trail climbs beneath towering pines. To the northeast is an old hunter's camp; "
                    "to the northwest, a cliff path rises toward a ruined observatory."
                ),
                exits={"south": "Crossroads", "northeast": "Hunter Camp", "northwest": "Observatory Steps"},
            ),
            "Hunter Camp": Room(
                name="Hunter Camp",
                description=(
                    "A cold firepit, snapped bowstrings, and a locked satchel remain. "
                    "A brass key hangs from a tent peg."
                ),
                exits={"southwest": "Forest Trail"},
                items=["brass key"],
                lore="Hunters served as wardens of the marsh gate in ages past.",
            ),
            "Observatory Steps": Room(
                name="Observatory Steps",
                description=(
                    "Broken stone steps lead to a bronze door with a dry lamp basin beside it. "
                    "Without fuel, the celestial mechanism will not awaken."
                ),
                exits={"southeast": "Forest Trail", "up": "Starlit Observatory"},
                locked_exits={"up": "item:lantern oil"},
            ),
            "Starlit Observatory": Room(
                name="Starlit Observatory",
                description=(
                    "Ancient lenses crown the chamber. A star dial projects symbols over the floor:\n"
                    "'Name what rises each dawn, yet is never the same twice.'"
                ),
                exits={"down": "Observatory Steps"},
                puzzle=Puzzle(
                    puzzle_id="sun_riddle",
                    prompt="Name what rises each dawn, yet is never the same twice.",
                    answers=("sun", "the sun"),
                    reward="star sigil",
                ),
                lore="The astronomers forged sigils to synchronize the sanctum wards.",
            ),
            "Ruins Gate": Room(
                name="Ruins Gate",
                description=(
                    "Crumbling arches guard the archive wing. A plaque reads:\n"
                    "'I speak without a mouth and hear without ears. What am I?'"
                ),
                exits={"west": "Crossroads", "east": "Archive Hall"},
                puzzle=Puzzle(
                    puzzle_id="echo_riddle",
                    prompt="I speak without a mouth and hear without ears. What am I?",
                    answers=("echo",),
                    reward="crystal shard",
                ),
                locked_exits={"east": "puzzle:echo_riddle"},
            ),
            "Archive Hall": Room(
                name="Archive Hall",
                description=(
                    "Collapsed shelves form a maze of parchment and stone. At the center lies a silver compass "
                    "engraved with valley constellations."
                ),
                exits={"west": "Ruins Gate", "north": "Sanctum Gate"},
                items=["silver compass"],
            ),
            "Marsh Path": Room(
                name="Marsh Path",
                description=(
                    "Fog drifts over black water and reeds. A heavy iron lock secures the caveward floodgate."
                ),
                exits={"east": "Crossroads", "west": "Cave Mouth"},
                locked_exits={"west": "item:brass key"},
            ),
            "Cave Mouth": Room(
                name="Cave Mouth",
                description=(
                    "The cave breathes cold mist. Darkness swallows the inner tunnel unless your lantern can be fueled."
                ),
                exits={"east": "Marsh Path", "west": "Deep Grotto"},
                locked_exits={"west": "item:lantern oil"},
            ),
            "Deep Grotto": Room(
                name="Deep Grotto",
                description=(
                    "Bioluminescent fungi glitter on wet stone. A pedestal of obsidian cradles a warm, radiant sun gem."
                ),
                exits={"east": "Cave Mouth", "north": "Sanctum Gate"},
                items=["sun gem"],
            ),
            "Sanctum Gate": Room(
                name="Sanctum Gate",
                description=(
                    "A colossal door rises before you. Four sockets await relics from ruins, marsh, archives, and stars."
                ),
                exits={"south": "Deep Grotto", "southwest": "Archive Hall", "north": "Final Sanctum"},
                locked_exits={"north": "set:final_relics"},
            ),
            "Final Sanctum": Room(
                name="Final Sanctum",
                description=(
                    "Relic light floods the sanctum dome. Ancient wards flare alive and the valley wind grows warm again. "
                    "You have restored the seal and become Keeper of Echoes. You win!"
                ),
                exits={},
            ),
        }

    def describe_current_room(self) -> str:
        room = self.rooms[self.state.current_room]
        lines = [f"\n== {room.name} ==", room.description]
        if room.items:
            visible_items = [item for item in room.items if item not in self.state.inventory]
            if visible_items:
                lines.append("Items here: " + ", ".join(visible_items))
        if room.puzzle and room.puzzle.puzzle_id not in self.state.solved_puzzles:
            lines.append(f"Puzzle: {room.puzzle.prompt}")
        lines.append(f"Exits: {', '.join(room.exits.keys()) if room.exits else 'none'}")
        return "\n".join(lines)

    def _requirement_met(self, requirement: str) -> bool:
        if requirement.startswith("item:"):
            item = requirement.split(":", maxsplit=1)[1]
            return item in self.state.inventory
        if requirement.startswith("puzzle:"):
            puzzle_id = requirement.split(":", maxsplit=1)[1]
            return puzzle_id in self.state.solved_puzzles
        if requirement == "set:final_relics":
            return self.final_relics.issubset(self.state.inventory)
        return False

    def _requirement_hint(self, requirement: str) -> str:
        if requirement.startswith("item:"):
            return f"You need: {requirement.split(':', maxsplit=1)[1]}"
        if requirement.startswith("puzzle:"):
            return "A sealed puzzle blocks this path. Solve the local riddle first."
        if requirement == "set:final_relics":
            missing = sorted(self.final_relics - self.state.inventory)
            return "The sanctum rejects you. Missing relics: " + ", ".join(missing)
        return "The way is sealed by ancient magic."

    def process_command(self, raw: str) -> str:
        cmd = raw.strip().lower()
        if not cmd:
            return "Type a command. Try: help"

        if cmd in {"quit", "exit"}:
            self.state.flags["lost"] = True
            return "You set down the quest and leave the valley to its silence. Game over."

        if cmd in {"help", "?"}:
            return (
                "Commands: look, go <direction>, take <item>, solve <answer>, inventory, lore, status, help, quit"
            )

        if cmd in {"look", "l"}:
            return self.describe_current_room()

        if cmd in {"lore", "read"}:
            room = self.rooms[self.state.current_room]
            return room.lore if room.lore else "There is no readable lore here."

        if cmd in {"status"}:
            solved = len(self.state.solved_puzzles)
            return f"Location: {self.state.current_room} | Puzzles solved: {solved} | Relics: {len(self.state.inventory)}"

        if cmd in {"inventory", "i"}:
            if not self.state.inventory:
                return "Your inventory is empty."
            return "You carry: " + ", ".join(sorted(self.state.inventory))

        if cmd.startswith("take "):
            item_name = cmd[5:].strip()
            room = self.rooms[self.state.current_room]
            if item_name in room.items and item_name not in self.state.inventory:
                self.state.inventory.add(item_name)
                return f"Taken: {item_name}."
            if item_name in self.state.inventory:
                return "You already took that item."
            return "That item is not here."

        if cmd.startswith("solve "):
            answer = cmd[6:].strip()
            room = self.rooms[self.state.current_room]
            if not room.puzzle:
                return "There is no puzzle here."
            puzzle = room.puzzle
            if puzzle.puzzle_id in self.state.solved_puzzles:
                return "This puzzle is already solved."
            if answer in puzzle.answers:
                self.state.solved_puzzles.add(puzzle.puzzle_id)
                reward_line = ""
                if puzzle.reward:
                    self.state.inventory.add(puzzle.reward)
                    reward_line = f" You gained: {puzzle.reward}."
                return f"Correct. Ancient mechanisms shift and unlock paths.{reward_line}"
            return "Incorrect. The mechanism hums but remains locked."

        if cmd.startswith("go "):
            direction = cmd[3:].strip()
            room = self.rooms[self.state.current_room]
            if direction not in room.exits:
                return "You cannot go that way."

            requirement = room.locked_exits.get(direction)
            if requirement and not self._requirement_met(requirement):
                return self._requirement_hint(requirement)

            self.state.current_room = room.exits[direction]
            if self.state.current_room == "Final Sanctum":
                self.state.flags["won"] = True
            return self.describe_current_room()

        return "Unknown command. Type 'help' to see available commands."

    def is_over(self) -> bool:
        return self.state.flags["won"] or self.state.flags["lost"]


def main() -> None:
    game = TextAdventureGame()
    print("Welcome to Echoes of the Valley: Extended Edition")
    print("You must recover four relics and restore the sanctum seal.")
    print("Type 'help' for commands.")
    print(game.describe_current_room())

    while not game.is_over():
        command = input("\n> ")
        print(game.process_command(command))


if __name__ == "__main__":
    main()
