# 🕹️ CoreEngine-2D: High-Performance Systems-Driven Roguelike Engine

A custom, highly optimized 2D game engine built from scratch in Python and Pygame. This project showcases advanced game architecture, clean code principles, and deliberate systems design aimed at maximizing CPU efficiency within a single-threaded execution environment.

Instead of relying on high-level commercial engines, this project implements core architectural patterns—such as time-spliced request throttling, hybrid spatial partitioning, dynamic state rehydration, and an adaptive AI Director—directly to practice production-grade software engineering and performance optimization.

---

## 🚀 Key Architectural Showcases

### 1. Hybrid Spatial Partitioning & Query Filtering
* **The Problem:** Broad-phase proximity scans (e.g., checking which enemies are near an explosion or sound source) typically trigger expensive $O(N^2)$ nested distance checks, causing severe performance degradation as the entity count scales.
* **The Solution:** A dual-layer hybrid search system (`Find_Nearby_Enemies`) that dynamically selects the mathematically optimal algorithm based on the query radius.
* **Technical Details:**
  * **Short-Range Queries ($\le 10$ units):** Bypasses entity-list iteration entirely by utilizing an $O(1)$ grid-based spatial partition system via the tilemap array, querying only local, neighboring tile indices.
  * **Long-Range Queries ($> 10$ units):** Transitions to a localized linear scan utilizing **squared Euclidean distance** ($dx^2 + dy^2 < \text{radius}^2$), avoiding the massive CPU overhead of square-root calculations (`math.sqrt`) inside the loop.

### 2. Asynchronous Time-Spliced Pathfinding Queue
* **The Problem:** Processing heavy A* pathfinding requests for 50+ of enemies on the exact same frame causes massive micro-stutters and dropped frames.
* **The Solution:** Implemented a decoupled **Load-Balanced Request Queue** (`Enemy_Pathfinding_Handler`) that throttles and distributes heavy calculations over time across multiple frame steps.
* **Technical Details:**
  * Leveraged `collections.deque` for $O(1)$ constant-time element extraction (`popleft`), bypassing the linear $O(N)$ memory shifting costs of standard Python arrays.
  * Features dual processing streams: a high-priority, proximity-sorted queue for aggressive combat targets, and a relaxed, low-frequency queue for idling/patrolling entities.
  * **Batch Optimization:** Uses a frame-latch mechanism (`should_sort_queue`) to sort the queue at most *once* per frame execution tick, preventing the $O(N^2 \log N)$ computational spikes caused by sorting on every single element insertion.

### 3. Dynamic AI Director ("Awakening" System)
* **The Problem:** Traditional static spawning structures lead to predictable, flat gameplay pacing and high risk of entity-overflow performance degradation.
* **The Solution:** Engineered an architectural state-machine supervisor (`Awakening`) modeled after modern AI director patterns to dynamically regulate mechanical pressure.
* **Technical Details:**
  * Monitors real-time environmental stress indicators (active entity metrics, map density coefficients).
  * Uses a dynamic probability matrix (`random.choices` with moving weight configurations) that chokes off enemy spawns entirely when performance limits are neared, or doubles threat generation if the player clears areas too quickly.
  * Employs unified command execution patterns wrapped in parameterless execution closures (`lambda` handlers) to cleanly trigger world mutations safely.

### 4. Unified Serialization Pipeline & Memento Hub (`Save_Load_Manager`)
* **The Problem:** Saving or restoring state in a deeply interconnected game world often yields scattered, ad-hoc file I/O operations. This fragmentations creates "stale data injections," risks broken state syncing between dependent subsystems (e.g., mismatched player positions versus a modified world tilemap), and leaves lingering unlinked runtime files.
* **The Solution:** A centralized, atomic persistence layer that orchestrates game-wide snapshot captures. It consolidates independent subsystem data schemas into a single unified binary composite save-file.
* **Technical Details:**
  * **The Memento Pattern Variant:** Implements a centralized snapshot mechanism. It triggers deep state extractions across disparate game-state modules (`a_star`, `tilemap`, `enemy_handler`, etc.), tracking localized dictionaries via index-matched orchestration registries.
  * **Atomic Binary I/O Operations:** Bundles aggregated component layers into an absolute composite dictionary payload, executing non-blocking, zero-overhead file exports to a disk cluster via Python’s binary serialization layer (`pickle.dump` with `"wb"` flags).
  * **Defensive Lifecycle Protections:** Features pre-execution filesystem sanitization hooks (`os.remove`) with structured error boundaries. If an IO transaction fails, it catches exceptions safely to guarantee file integrity, preventing corrupt data injections from breaking the game's startup sequence.
  
### 5. Data-Driven Spawning Factory
* **The Problem:** Hardcoding level generation or specific biome entity arrays violates the *Open-Closed Principle*, making codebase expansion difficult and highly error-prone.
* **The Solution:** Implemented a decoupled polymorphic factory infrastructure (`Set_Spawner_Type`) that isolates biome data mapping from core game mechanics.
* **Technical Details:**
  * Dynamically maps level configurations directly to specific generator types (`Crypt_Spawn`, `Crystal_Cavern_Spawn`) using configuration lookups.
  * Sanitizes raw generation string keys using suffix-stripping logic (`.split('_')`) to isolate base types from instances, ensuring clean lookup tracking against structural dictionary functions.

### 6. Sub-Stepped Radial Light & Fog-of-War Raycaster
* **The Problem:** Standard tile-stepping vectors easily clip through 45-degree corner boundaries (diagonal light leaking), and linear step-decay results in diamond-shaped falloff matrices rather than accurate radial shapes.
* **The Solution:** A high-frequency dynamic lighting layer built using optimized trigonometrical lookups and distance-attenuation formulas.
* **Technical Details:**
  * **Hot Loop Optimization:** Pre-computes angle cosine/sine lookup arrays outside the rendering loop, localizing class methods to minimize instruction overhead during execution.
  * Implements sub-stepped vector sampling ($0.5$ tile increments) to completely eliminate diagonal wall penetration bugs.
  * Computes geometric decay utilizing true Euclidean distance calculations (`math.hypot`) for smooth circular falloff.
  
### 7. Immutable Flyweight State Engine (`Attribute_Distributor`)
* **The Problem:** Storing individual base balance stats directly inside every active enemy instance introduces redundant memory overhead. Furthermore, modifying an entity’s current health or strength directly on a shared template risks "variable pollution"—where updating one enemy accidentally mutates the traits of every other enemy of that type.
* **The Solution:** A decoupled scaling factory that treats base monster configurations as immutable prototypes. It reads static templates, processes progression math, and returns distinct state allocations.
* **Technical Details:**
  * **The Prototype/Flyweight Pattern:** Aggregates independent stat dictionaries (`SKELETON_STATS`, `VOID_SPAWN_STATS`) into a centralized lookup matrix. Instead of instantiating heavy default templates repeatedly, it treats them as read-only blueprints.
  * **Hot-Loop String Parsing Optimization:** Replaces expensive, on-the-fly regular expression compilation bottlenecks with a globally cached, pre-compiled regex structural pattern (`re.compile`). This safely optimizes string sanitization passes during heavy level generation and mass-spawning phases.
  * **Data Isolation via Immutability:** Leverages Python's `dataclasses.replace` to duplicate base profiles into standalone records with modified values. This ensures complete data isolation—meaning current entity variables remain strictly separate from baseline global profiles.

### 8. Hierarchical Composite Inventory & Drop Director (`Item_Handler`)
* **The Problem:** Scaling item sub-categories (weapons, runes, potion consumables) within a centralized manager often causes monolithic code bloat and unmaintainable state branching logic.
* **The Solution:** A decoupled **Composite Design Pattern** framework that acts as a single gateway interface while handing off generation logic to localized, item-specific handlers.
* **Technical Details:**
  * **Adaptive Pacing & Loot Economy:** Implements an evaluation scanner (`Adjust_Weights`) that queries the player's inventory cache in real time. It dynamically warps drops based on current state coefficients—such as dropping key drop rates to 0% if one is already carried, or spiking key drops to 50% if the player is stuck.
  * **The Facade Pattern:** `Item_Handler` exposes a single, unified interface for spatial proximity checks, item clearing, and loading sequences, abstracting away the complex internal logic of `Rune_Handler`, `Weapon_Handler`, and `Loot_Handler`.
  * **Proximity Scan Throttling:** Features a delta-time cooldown gate (`Update_Nearby_Items_Cooldown`) that limits expensive spatial tile queries to fixed 0.5-second intervals, preserving CPU cycles during intense combat phases.
  
### 9. Flyweight Grid Matrix & Cellular Extraction Engine (`Tilemap` & `Tile`)
* **The Problem:** Naively instantiating a unique high-level object for every individual tile in a massive game world rapidly degrades memory performance. Additionally, parsing entire map grids to extract specific entities (e.g., finding all gold or spawn points during initialization) causes heavy performance bottlenecks.
* **The Solution:** A high-performance spatial grid system that treats static structural cells as lightweight, multi-layered data points, paired with a specialized entity extraction lookup pipeline.
* **Technical Details:**
  * **The Flyweight Pattern for Grid Maps:** Separates structural layout definitions from variable runtime objects. Instead of bloating every coordinate cell with duplicate graphic references or texture matrices, tiles retain localized index vectors mapped against a centralized tile dictionary layout.
  * **Layered Key Filtering & Token Extraction (`extract`):** Bypasses blind nested loops across grid dimensions via a optimized lookup array mechanism. Subsystems pass unique signature tokens (e.g., `[(keys.gold, 0)]`) to extract matching elements dynamically while clearing structural tiles simultaneously, avoiding duplicate tracking registries.
  * **Spatial Entity Dereferencing:** Features explicit entity tracking registers tied directly to the cell grid structure (`Remove_Entity_From_Tile`). This ensures that physics layers, item drops, and raycasting systems can execute focused, localized tile searches rather than scanning broad, scene-wide coordinate lists.
  
## 🏗️ Architectural Blueprint & Design Patterns

The engineering foundation of this engine relies on a strictly decoupled, composition-over-inheritance architectural philosophy. By isolating distinct execution domains, the system achieves predictable state mutation, straightforward maintainability, and horizontal scalability.

### 1. Object Pool & Manager Pattern (`Enemy_Handler`)
* **Context:** Creating, garbage collecting, and destroying high-level Python class instances frequently during runtime triggers costly memory overhead and unpredictable garbage collection spikes.
* **Implementation:** The `Handler` classes acts as a centralized object repository and lifecycle hub. 
* **Design Advantage:** * Instantiates entities inside a controlled, reusable list pool.
  * Completely decouples entity lifecycles from system handlers. When an entity dies, used or otherwise deleted, the manager cleanly unlinks it across all tracking layers simultaneously (rendering pipelines, pathfinding queues, and spatial indices), preventing dangling references, ghost execution updates, and memory leaks.

### 2. Polymorphic Spawner Factory Method (`Set_Spawner_Type`)
* **Context:** Hardcoding environmental configurations or map-specific generation rules creates tight coupling, breaking the *Open-Closed Principle* and forcing sweeping codebase updates whenever a new level tier or biome is developed.
* **Implementation:** Implemented an extensible abstract factory lookup infrastructure mapping system configurations to localized generator contexts (e.g., `Crypt_Spawn`, `Crystal_Cavern_Spawn`).
* **Design Advantage:** The core game loop never needs to know *what* specific enemy variants are spawning or *how* they are structured. It simply invokes the assigned factory interface. Adding a new biome is completely risk-free and achieved simply by registering a new spawner type mapping to the dictionary layout.

### 3. Command Pattern Closure Execution (`Awakening`)
* **Context:** The AI Director must execute a wide array of completely unrelated world-mutating events (spawning elites, debuffing players, locking doorways) through a unified execution interface without creating massive, unmaintainable nested `if/elif` branching blocks.
* **Implementation:** Encapsulated environmental modifications inside a Command Pattern structure, routing event triggers directly into parameterless execution closures (`lambda` expressions).
* **Design Advantage:** Isolates the system selector from target object signatures. The execution pipeline invokes a uniform `awakening_function()` call, leaving signature validation and argument isolation safely compartmentalized inside individual event objects.

### 4. Component Composition Over Inheritance (`Enemy` Sub-Systems)
* **Context:** Relying on deep class inheritance hierarchies (e.g., `Entity -> MovingEntity -> CombatEnemy -> Skeleton`) leads to rigid code structures where units inherit bloated, unused logic and components cannot easily adapt during runtime.
* **Implementation:** Replaced heavy inheritance branches with decoupled component handlers (`Status_Effect_Handler`, `Behavior_Manager`, `Movement_Strategies`) instantiated inside base entity wrappers.
* **Design Advantage:** Grants the engine immense flexibility. Behavior and movement rules are isolated as hot-swappable strategies. Units can dynamically shift states, swap out movement modes, or gain and lose active status modifiers on the fly without changing their underlying class layout.