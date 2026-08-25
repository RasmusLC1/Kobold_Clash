# Kobold Clash

A 2D roguelike dungeon crawler built from scratch in Python and Pygame — no external game engine, no third-party ECS or physics library. Enemy AI, pathfinding, lighting, save/load, and level generation are all hand-rolled.

I started this in August 2024 and have kept working on it since, on and off, treating it partly as a real product I'd like to eventually release, and partly as a space to practice building and maintaining a codebase the way I would at work — with tests, PR-style self-review, and refactors instead of rewrites.

---

## Why build the engine instead of using one

Mostly because I wanted to actually understand the problems a game engine solves for you, rather than just use the solution. A* pathfinding for 100+ enemies without stuttering, tile-based fog-of-war lighting that doesn't leak through corners, saving a deeply interconnected game world without corrupting it — these are the kinds of problems that are easy to wave away with "the engine handles that," and I wanted the version of this project where I couldn't wave them away.

The trade-off is honest: this took a lot longer than using Godot or Unity would have, and some systems here (the earlier ones, in particular) show it. I'd rather that be visible than hidden.

---

## Systems worth looking at

### Enemy AI and the pathfinding queue
`Enemy_Handler` owns the lifecycle of every enemy — spawning, updating, and tearing down references across every subsystem that tracks them (render layer, pathfinding queues, acoustic/clatter listeners) so nothing gets left dangling when an enemy dies.

The part I'm most happy with is `Enemy_Pathfinding_Handler`. Running full A* for 50+ enemies on the same frame causes visible stutter, so requests get distributed across frames instead of solved all at once, using a `deque` for O(1) queue operations and two separate priority streams — one for enemies actively chasing the player, one low-priority stream for idle patrolling so it never competes with combat pathing. Sorting the combined queue is throttled to once per frame via a simple boolean latch, rather than re-sorting on every single insertion.

### Registries instead of subclassing
Enemies, decorations, traps, and abilities all used to be registered by hand — a per-dungeon subclass with its own hardcoded dict of types. That worked, but adding a new dungeon meant writing a new subclass, and adding a new type inside an existing dungeon meant editing that subclass's constructor. It didn't scale well and it violated open/closed pretty directly.

I refactored all four systems onto the same pattern: a decorator (`@register_trap`, `@register_ability`, etc.) that a class uses to register itself into a plain dict at import time, a small "shared vs. dungeon-specific" merge step, and a `load_all.py` per package whose only job is importing every module in that category so its decorator fires. Adding a new trap now means writing the trap class and adding one import line — nothing in the spawner itself changes.

It's not free. Decorator-based registration trades loud failures for quiet ones — a missing import means a type silently doesn't exist rather than an obvious crash, and getting the import ordering wrong reintroduces circular imports that are genuinely annoying to trace back to their actual cause. I hit that a few times while building this out. I think the trade-off is worth it for a project that's still actively growing its content, but it's not something I'd reach for unconditionally.

### Fog-of-war raycasting and lighting
360° raycasting for visibility, with per-light-source additive tile lighting layered on top. The two things that were actually hard here: stepping the rays in half-tile increments so a diagonal wall corner can't be seen through, and using true Euclidean distance for falloff so light reads as a circle instead of a diamond. Angle lookups are precomputed outside the render loop since this runs every frame.

### AI Director ("The Awakening")
Loosely inspired by Left 4 Dead's director — it watches how much noise the player is making and how dense the current room is, then leans on spawn rates and trap density in response, rather than following a fixed script. Mechanically it's a state machine that dispatches to a set of world-mutation functions based on a weighted table that shifts over time.

### Save/load
Every subsystem that owns persistent state (pathfinding, tilemap, enemies, decorations, traps) implements its own `Save_Data`/`Load_Data`, and a central manager collects all of it into one dictionary and writes it with `pickle`. Nothing fancy, but it's consistent across every subsystem and I made a point of guarding the file write so a crash mid-save can't leave a corrupted file blocking the next launch.

### Status effects
Effect types (poison, freeze, slow, etc.) are defined once in a class-level registry and instantiated lazily — an entity only pays for a `Poison` instance the first time it's actually poisoned, and that instance is cached and reused after. Some effects read each other's state directly (frozen entities take double duration if they're already wet, stacked fire damage scales with stack depth) rather than going through a central coordinator, which keeps the interactions simple to write but means the coupling between effects is implicit — worth knowing if you're reading that code.

---

## What's still rough

Being upfront about this rather than hiding it: the newer systems (enemy AI, the registries, lighting) reflect how I'd approach this today. Inventory and weapon handling are from earlier in the project and haven't had the same pass yet — they work, but the patterns are older and I know they need a refactor. I'd rather flag that than have someone find it and wonder if I don't see it.

Test coverage is real but uneven — pathfinding, tilemap queries, raycasting, and status effects have solid pytest coverage with a mocked game context.

---

## Running it

*(setup instructions — Python version, `pip install -r requirements.txt`, how to launch)*

## Tech

Python, Pygame, pytest.
