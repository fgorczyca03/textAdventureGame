# Text Adventure Game: Echoes of the Valley (Extended Edition)

`Echoes of the Valley` is a **console-based Python text adventure** with a larger world map, layered progression, and richer story flavor.

## What’s Included

- **Branching world design** with multiple paths and revisit-friendly room graph
- **Inventory-based progression** with utility items and relic collection
- **Multiple puzzles** that unlock routes and grant key rewards
- **Lore command** to read environmental story snippets in specific locations
- **Status tracking** to view current location, solved puzzles, and inventory progress

## Quick Start

```bash
python3 game.py
```

## Commands

- `look` or `l` — describe the current room, visible items, puzzle prompt, and exits
- `go <direction>` — move to another room if the path is unlocked
- `take <item>` — pick up an item in the current room
- `solve <answer>` — answer the active room puzzle
- `inventory` or `i` — list carried items
- `lore` — read room-specific narrative details
- `status` — show progress summary
- `help` — print command list
- `quit` — leave the game

## Deeper Gameplay Notes

- Some paths require an **item** (for example, the marsh floodgate and dark cave).
- Some paths require a **puzzle to be solved first**.
- The final sanctum requires a **full relic set**:
  - `crystal shard`
  - `sun gem`
  - `silver compass`
  - `star sigil`

## Suggested First Route

1. Visit the village to find `lantern oil`.
2. Explore the forest to collect the `brass key`.
3. Solve the observatory and ruins riddles.
4. Recover relics in archive and cave branches.
5. Return to the sanctum gate and unlock the final chamber.

## Run Tests

```bash
python3 -m unittest discover -s tests -v
```
