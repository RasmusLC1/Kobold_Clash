Game Ideas

LOADING PAGE:
Menu screen that renders parts of a loading bar every time a step in dungeon generator generates a new chunk
Save it in a seperate class that accepts an increment from dungeon generator


# Dungeon Crawler Gameplay Ideas
    Can find weapons, magic items and runes
    There are layers to the dungeon, each layer have one exit and different staircases down to a new random dungeon. You cannot go up through the original entrance again
    Clatter system that spawns enemies using a director similar to left4dead
    Each dungeon layer get's progressively harder, but main challenge is to conserve resources to proceed further down
    Each section has at least 1 random combat from a pool of possible mobs based on enviorement, freeze section as freeze enemies
    Each layer draws a random theme, fire for example, then it draws from the tech theme for example
    Noice attracts enemies

# Gameplay Loop
    Choose between 2 modes, descend or endless. Decent takes you through 7 layers of the dungeon to a final boss
    Collect gold and artifcats in dungeon to buy items, upgrades, healing etc
    Lower levels have better rewards
    To get to lower levels you need to pay a soul cost on each floor
    Each time you complete a floor the next one becomes more difficult
    There are shrines in the dungeon where you can pay with souls of slain enemies to buy upgrades
        Shrines are found in boss rooms, risk damage to upgrade
        Different Shrines do different things:
            Rune shrine, Upgrade and Buy runes
            Character shrine, upgrade character
            Artifact Shrine, buy and upgrade weapons and artifacts
        Boss Room initialised as an object with a radius, closes doors and locks player in.
            Spawns boss mob when player is x from center
            Spawns Shrine when boss mob is defeated
        
    Game ends when you die, you can find resurrection items in the dungeon, but they are rare or high risk
        

# Engine Features:
    # Tile systsem
    # Use A* for path finding
    # Inventory System
    # Weapon inventory system
    # Dropping item, triggers trap
    # Raytracer that limits players vision, so enemies can sneak up from behind
    # Light engine
    # Clatter System where enemies are attracted to noise
    # Dungeon generator
    # Chunk system to prevent slowdown with larger maps
    # Save Load System
    # Particle Engine
    Sound engine
    Minimap, adjust rendering scale for minimap and only display tiles that has been in raycaster
    Threat metre, a skull that fills up or something. If player generates clatter it has a chance to increase. It will also have a chance to decrease if player is quiet for longer periods of time

# Gameplay
    # Player can hold weapons
    # Attack
    # Defend
    X chance to get a shop each floor, spawns similar to boss room
    In shop you can upgrade weapons, buy items, heal, etc
    Get points upon death based on level depth, gold and relics

# Shop
Buy and sell items to help complete levels
Upgrade weapons


# Atmosphere
     dynamic sound elements: distant whispers, creaky floorboards, enemy sounds.
     Particle effects on screen like dust

# Clatter engine
    Generating clatter has a chance to increase the difficulty of the dungeon layer

    Increasing difficulty can have the following effects
        - Spawn enemies
        - Add traps
        - Give player debuffs
        - Buff enemies
        - Replace doors with walls
        - Replace chests with mimics
        - Reduce light level of all light sources
        - Spawn elite enemies
        - Increase overall clatter level, which increases the consequence of the other effects
        
    Clatter always notifies nearby enemies

    Add skull that gradually fills up with clatter level, hover over for clatter level

    When clatter is generated and has a negative effect apply screen shake and particles on the screen to simulate dungeon shaking and a deep rumble sound

    5 clatter levels, each has different probabilities for events, the higher the clatter level the worse the consequences

    Higher clatter levels generate better loot spawns as well


# Weapons:
    Weapons have health, forcing players to either repair them with ingots at weapon shrines or to get new weapons 
    Weapons have a pool of damage stats, so for instance a sword might have a dictionary with fire, frozen, sharpness and the damage value of each effect
    Weapons can be upgraded with gems
    # Implement better animations, bright arcs for where the damage area is
    # Torch, emits light and be be used to set enemies on fire, relatively low damage
    # Sword, best damage, little utility
    # Spear, can be thrown
    # Shield, can block damage, can be used to rocket jump with bomb
    # Bow, can press button, different arrows that can do certain things
    # Axe, can break wood doors
    # Hatchet, small axe, faster than axe
    # Mace/Hammer, can break certain walls and enviorement, special ground pound to stun nearby enemies
    # Halberd, swing and stab attack, charge attack
    # Scythe, swing attack, soul reap magic attack
    # Crossbow, Same as bow, but takes longer to load, but can be preloaded
    # Bomb, one time use, splash damage, can break enviorement, knockback from blast
    magic Staff, improved runes but poor melee damage, different staffs for different lores of magic, costs souls per cast. Special attack for each lores

# Items
    Items are held in inventory, not worth a lot of money, but helps navigate dungeon
    Rare objects found in loot rooms
    
    
    ## Permanent:
        # Lantern, Sets the player light to 7, passive light
        # Magnet, autopickup of items
        # Totem of Power, increases Rune power, stacks with more totems
        # Totem of Strength, increases strength
        # Anchor Stone – Prevents the player from being pushed by traps or enemies.
        # Muffled boots – Reduces the noise generated by movement.
        # Halo, 1/10 chance to cancel damage
        # Echo Sigil, increases the activations of items by 1
        # Recipe scroll, increase potion strength by + 1, works similar to echo sigil
        Compass that points towards boss room
        Lucky Charm, Improves chest loot
        Pendant of Faith, Highlights traps, Needs trap rework first
        Different types of Cursed Talisman, Gives scaling benefits for each curse, maybe 10% movement increase for 1 curse, 20 for 2 etc
        Shrine hunter items, increases an effect for each shrine visited, health, strength, speed etc.
        Greed echo that gives gold when clatter is generated (needs cooldown to prevent spam), tied to enemies attracted
        Soul echo, same as Greed echo 


    # Triggered:
        # Pendant of light, Revive on death for souls 
        # Phoenix Feather – Upon death, revives the player with 1 health, then burns up.
        # Gravedigger’s Coin – Revive the player one time to full health for 100 gold
        # Blood Pact Scroll – Allows revival at the cost of a permanent debuff.



    ## utility:
        ### Keys:
            # lockpick, has a 1/3chance to open the door and persist
            # Skeleton Key – Unlocks any door but disappears after 1 use
            # Blood Key – Unlocks any door but costs health
            # Soul Key – Unlocks any door but costs souls
            # Cursed Key – Unlocks any door but gives a random curse


        # Echo Bell – Creates a noise at a targeted location to lure enemies away.
        # Cloak of Shadows – Temporarily makes the player invisible to enemies.
        # Faded Hourglass – Slows down nearby enemies movement
        # Ethereal Chains – snares nearby enemies for a short duration.
        # Recall Parchment – Teleports the player back to the last shrine visited.

        Torch of Guidance - Reveal the portal shrine on minimap
        Rope Hook – Can be thrown to pull the player across gaps.
        Alchemy Flask – Randomly turns a minor item into another item upon use.
        Dungeon Map Fragment – Reveals part of the current dungeon layer.

    ## Combat item
        # electric Bomb – electric explosion
        # Fire Bomb – Fire explosion
        # Frozen Bomb – Frozen Explosion
        # Poison Bomb – Poison Explosion
        # Vampiric Bomb – Vampiric Explosion
        Oil Flask – Can be thrown to create a flammable puddle.
        Holy Water – Weapons deals extra damage to undead and ghosts.
        Hexing Charm – Weakens the next enemy hit, cooldown.
        Hunter’s Fang – Increases weapon damage against beasts.
    
    ## Cursed Items:
        Items are soul bound, meaning destroyed when dropped
        # Blood tomb, Gain souls when damaged
        # Demonic Bargain – Increases damage output but prevents healing
        # Temptress Embrace - Reduces damage output when health > 50% but increases below 50%
        Black Coin – Increases gold earned but increases damage taken
        Vampire’s Locket – Grants lifesteal but slowly reduces max health over time.
        Cursed Dice – Rerolls effects to be random, but weighted for positive effects
        Eldritch Mirror – Reflects a portion of damage taken but doubles negative status effect duration.
        Forsaken Grimoire – Increases rune power but randomly casts negative effects on the player
        Cracked Talisman – Grants resistance to elemental damage but causes physical damage to double
        Echoing Skull – Reveals hidden secrets in the dungeon but whispers eerie sounds, attracting enemies

    ## Gems
        Different gems that gives attributes to weapons, also valuable to sell
        # fire - Set fire effect on weapon
        # freeze - Set freeze effect on weapon
        # poison - Set poison effect on weapon
        # vampiric - Set vampiric effect on weapon
        # electric - Set electric effect on weapon
        # Arcane hunger - Set Arcane hunger effect on weapon
        # blunt - Set blunt damage on weapon
        # slash - Set slash damage on weapon
        # halo - Grants wielder a chance to protect from damage
        # power - Increases rune power while equipped
        # range - Increases weapon range
        # resistance - Chance for weapon not to take damage
        # speed - Increases weapon attack speed
        # strength - Increases wielders strength
        # terror - Chance for enemies to run away
        # vulnerable - Entities hit take extra damage
        # weakness - entities hit gets weakness
        # wet - Set wet effect on weapon, can combo with electric, water and fire (steam)
        # durability - Increases weapon health
        multishot - Fires two arrows at a time

    ## Ingots
        Can be used to repair items and add upgrades, also have high value at market depending on rarety
        Steel ingot - repairs weapons
        Jade ingot - repairs runes
        copper ingot - repairs items
        Gold ingot - can add gem slots
        Silver ingot - can upgrade rune power


    ## Potions
        # Based on player effects
        # Health
        # strength
        # movement
        # Soul
        # health regen, more health than health potion but slower
        # silence
        # invisibility
        # poison resistance
        # fire resistance
        # freeze resistance
        luck
        # vampire, heals based on damage dealt


# Runes
    You can have 3 runes equipped at a time
    Can buy new runes or upgrade existing ones in shrines 

    Costs souls each time it's cast
    Two types of runes, passive runes and activated runes
    Passive runes don't cost souls, but they are less powerful
    Active runes:
        # Dash,
        # Healing
        # Speed
        # Invisibility
        # Silence
        # Door unlock
        # Speed
        # Strength
        # Immunity
        Random Teleport, to get out of bad situations
        Scream, make enemies run away from you
        Shield charm, have 4 shield around you that grant immunity but breaks when damage taken
        # Vampiric, regen from damaging enemies
    
    Passive Runes:
        # Regen
        # Light
        # Arcane conduit, increase power level of your other runes
        # arcane_Hunger, increase souls generation
        # Magnet, Auto pickup of items
        # Resistance
        Thorns, enemies take damage when they hit you
        Frost Shield, enemies freeze when damaging you

    Fire runes:
        # Fireball, ball of fire that leads to fire explosion
        # Fire spew, flamethrower attack
        Fire wall, wall of fire that damage anything that tries to cross it
    
    Frost runes:
        # Iceball, ball that causes a freeze explosion that slows everything in it
        # Ice projectiles, fast ice projectiles shot like a bullet
        ice storm, Creates a tornado on entity that shoots ice projectiles at random 

    Electric runes:
        # Chain ligtning, Lightning projectile that bounces between entities
        # Electric ball, electric ball that generates electric explosion
        # Electric homing particle, electric projectiles that target nearest entity

    Poison runes:
        # Poison ball, Poison ball that turns into a poison cloud
        # Posion cloud, creates a big poison cloud around entity, area of effect
        # Poison plumes, creates  poison clouds around entity at random positions

    Vampiric runes:
        Life drain, slowly drain health from all nearby entities
        # Soul reap, broad projectile that sucks health from everything it hits
        # Soul pit that pulls entities in and sucks health from them

# Arrows:
    # Basic Arrow, Higher base damage
    Rope arrow, allows you to cross traps
    Fire arrow, lights enemies on fire and lights up the envoirement
    Ice arrow, ice effect, if it touches water it freezes the water
    Poison arrow, poison effect, if it touches water it poisons it
    Electric arrow, electric effect, triggers traps and electrifies water

# Movements:
    # Dash, Move rapidly without hit detection to a location
    # Roll, avoid damage and roll in the direction of the mouse
    # Backstep, move backwards a little and be immune
    # Block, block damage, if the player has shield block all damage, if not then it only blocks melee

    Teleport to a random destination, has x amount of charges
    Jump, can jump over 2 blocks with light armour, 1 with medium and 0 with heavy, takes stamina
    Swim in deep water, can't cross if in heavy armour
    Push certain objects and block

# Effects:
    # Fire – Burns the entity over time, dealing continuous damage.
    # Poison – Deals damage over time, but slower than fire.
    # Frozen – Slows movement speed and attack speed, may completely immobilize if stacked.
    # Wet – Makes the entity take extra damage from electric attacks and reduces fire damage.
    # Regeneration – Slowly restores health over time.
    # Speed Boost – Increases movement speed for a duration.
    # Strength Boost – Increases melee attack damage.
    # Invisibility – Makes the player undetectable by enemies unless they attack or make noise.
    # Fire Resistance – Reduces or nullifies fire damage.
    # Poison Resistance – Reduces or nullifies poison effects.
    # Frozen Resistance – Reduces or nullifies freeze effects.
    # Electric Charge – Causes electric attacks to arc to nearby enemies.
    # Silence – Prevents the affected entity from casting spells or using magic-based attacks.
    Luck Boost – Increases the chance for critical hits, rare drops, or dodging attacks.
    # Vampirism – Heals based on damage dealt.
    # Shielded – Grants temporary immunity to damage until shield is broken.
    # Thorns – Reflects damage back to attackers.
    # Magnetized – Automatically attracts loot, gold, and items.
    Soul Leech – Drains the souls of slain enemies for additional effects.
    Terror – Makes enemies flee from the player.
    # Slow – Reduces movement and attack speed.
    # Curse – Lowers stats temporarily or causes random negative effects.
    # Confusion – Inverts enemy movement or attack patterns.
    # Stone – Immobilizes but provides high defense.
    Sleep – Puts the affected entity in a sleep state until hit.
    # Snare – Stops movement for a short period.
    # Arcane conduit - Reduce the cost runes
    # Arcane_Hunger - Gain souls from entity kills

# Traps:
    # Spike pits, fall into and slows you down
    # Spike traps, that move up and harm you when they're extended
    # Spike traps poison, that move up and harm you when they're extended, poision effect
    # Fire traps, sets you on fire
    # Lava, sets on fire and slows down entity, heavy damage
    # Water, slows down entities
    # Ice decreases friction and accelaration
    Pressure plates that trigger effects
    Arrow traps - shoots arrows, triggered by pressure plates
    Loose rocks, generates clatter when stepped on
    


# Decorations
    - # Braziers with fire, lights up area, can be extinguished/ignited
    - # Pots and urns that can be smashed to get loot, generates clatter
    - Small rocks strewn around
    - Dust particles on the screen
    - # effogy tombs that can be opened for loot, but chance to spawn enemy
    - # Sacrifice shrine, sacrifice items of x value for bonus
    - # Hunter shrine, find specific item and sacrifice it for bonus. Opening the shrine spawns that item somewhere on the map and checks pathfinding to player
    - # Chest, standard loot, safe but multiple tiers that can determine the loot table
    - # Weapon racks, contains weapons
    - # Plinths, contains runes
    - # Libraries, with bookshelfs, sometimes contain runes and scrolls
    - # Laboratory, contains potions
    - # Soul well, harvest souls but can summon/attract enemies
    - False walls, can be destroyed to reveal treasure rooms
    - # Teleportation Circles, linked to each other, can be used to traverse the dungeon
    - # Teleport shrine, pay souls to teleport to a lower dungeon
    - # Rune shrine, pay souls to aquire new runes
    - Weapon shrine, pay souls to bind gems to weapons for bonuses increased bonuses
    - Fragile walls, can be broken by hitting with blunt weapons, acts as doors
    - Levers that spawn items, open doors etc when activated
    - Pressure plates, need to be held down to work, can be done with items. Works similar to levers
    - Shops where you can buy different items for gold, maybe a little kobold with a shop. Opens a menu, you can sell loot for gold and use gold to buy random selection of items


# Rooms:
    # Treasure room, contains loot
    # Library, contains bookshelves and potion tables
    Trapped room, contains traps but more valuable loot
    # Boss room, spawns a boss that then spawns a weapon or rune shrine when killed
    Lakes, can be any kind of elements



# Enemies:
    Enemies start out basic but can upgrade to elite as dungeon effects trigger
    Spawn enemies using dungeon director when effects trigger
    Enemies have a difficulty attribute to make the spawning dynamic
    Enemies seperated into tribes with different strengths and weaknesses
    - pack swarms the player
    - Solo, goes after the player alone
    - Scout, looks for and calls allies to attack the player
    - Sentry, calls enemies in a wide range to notify if they spot the player, but they don't move unless they see the player
    - Ambusher, waits and attacks the player
    - Support, supports the other enemies with healing
    - Ranged, shoots the player from range 
    - Melee, attacks the player up close


## Ancient Tomb Enemies
### Specialty
    Basic dungeon, used as introduction
### Enemies
    # Skeleton Warrior, basic warrior uses standard weapons
    # Skeleton scout, uses ranged weapons
    # Skeleton Cleric, heals undead in the area but does no damage
    # Skeleton Bell Toller, alerts nearby enemies if it sees the player
    # Skeleton Undertaker, revieves dead enemies
    # Skeleton Guard, slow, high health and medium damage
    # Skeleton warlock, uses magic poison attacks
    # Wight Lord, boss, armoured skeleton with shield and sword, can dash to close range
    # Banner bearer, Increases strength of nearby enemies
    # Phantom, immune to physical attacks, pathfinds directly to the target, phasing through walls, high damage, high speed and low health
    # Wraith, immune to physical attacks, pathfinds directly to the target, phasing through walls, low damage but steals soul (player mana), high speed and low health
    # Shade, immune to physical attacks, will always pathfind towards player, medium damage, low speed, low health
    # Vampire, boss, life steal, flying bat form when travelling, close combat
    # Crypt Ghoul, bone club, fast and high damage, but glass cannon
    Lich, casts doom on player, debuffing him and slowly drains health until Lich is killed

## Crystal Caverns
### Specialty
    Crystal Growth, walls occasionally dissapear or spawn changing the structure of the dungeon. Spawned walls can be broken
    Weapon gems spawn more often
### Enemies
    # Spider, shoots spiderweb that snares you, less damage
    Crystal Elemental, high health and strength, shoots crystal
    Minotaur, boss mob, charges and breaks envoirement, high damage, low defence
    Hydra, boss mob, splits head when a head is killed, needs to be attacked from behind or killed with enviorement damage
    Clicker, blind but good hearing, loud because of clicks
    Echo stalker, becomes visible for a time when clatter is generated
    Shard Wraith, teleports close to clatter source when clatter is generated
    Crystal golemn, slow and shoots crystal shards (similar to freeze shards)
    Crystal Scarab, basic enemy that swarms player
    Aurora Wisp, acts as light source, but might explode when clatter is triggered
    Medusa, shoots electric projetiles and fast but very low health
    Mirror crystal, reflects projectiles back at source by inverting angle
    Kobold, steals items from player and runs away

## Mycelium Depths enemies
### Specialty
    Mycelium network, clank is disabled. Instead enemies are aggroed by attacks or stepping on spore traps
    Potions spawn more often
### Enemies
    Fungal burrower, digs under the maps and attacks player from underground
    Unstable spore, charges and explodes if it touches the player with a short delay
    Sporeling, fast and small spores that attacks player
    Fungal brute, strong and slow mushroom creature, weak to fire
    Spore spitter, ranged enemy that shoots spores
    Poisioned spores, spawns poison plumes
    Glowcap Stalker, pretends to be a decorative mushroom and attacks when player is close, emits light
    Mycelium roots, snares the player
    Vitalcap, heals nearby enemies
    Gravebloom, hiding somewhere on the map. Needs to be killed to prevent enemies respawning
    Rot king, can snare player and spawns sporelings

## Serpents Lair
### Specialty
    Quatlz curse, player will slowly get more and more curse the longer they stay.
    Cursed items spawn more often
### Enemies
    Serpent Warriors, basic enemies that are decently strong individually
    Chameleons scouts, shoots poisoned darts, slightly transparent and difficult to spot
    Skink fanatics, high damage low health that charges the player aggressively
    Salamander hunters, shoots fire projectiles and high mobility, hunts in packs
    Temple guards, large crocodiles with high defence that aim to hold player in place
    Komodo priests, increases strength of nearby enemies
    Quetzalcoatl shaman, heals nearby enemies
    Ancient Tyrant, bos box t-rex, high damage and speed but low defence
    Embermaw, boss shoots fire from the front and has ball tail in back that can attack player, high defence and damage, but low movement 
    Great Python, constricts the player for a time allowing other enemies to attack
    Venomscale Lurker, posioned attack that jumps at player

## Titan Forge
### Specialty
    Ash storms, lowers visibility for a period of time at random
    Utility items spawn more often
    Better opportunity to upgrade weapons
### Enemies
    Magma warden, Molthen armor, high health and damage, but low speeds, sets player on fire if contact
    # Fire spirit, high speeds shoot flamethrower at close range and retreats
    Ash wraith, invisible until close then ignites and attacks player. High speed and damage, very fragile
    Ironbound demon, wraps player in chains to temporarily snare, low speed and damage, but high health
    Forge demon, revives fallen enemies
    Ember swarm, small enemies that swarm the player and do little damage, but dangerous in swarm
    Molten slug, immortal enemy that moves very slowly but very high damage if it touches player
    Phoenix, explodes when killed and revives itself. High speed, low damage and health
    Lava Lurker, hides in lava pools and jumps on the player, high damage and speed, but low health
    Ashen Tyrant , shoots burning chains out to attack player. Chains deal damage and pulls the player into lava traps.
    Forgeheart Titan, boss, shoots fireballs, high health and low speed. Area of effect attacks

# Glacial Caverns
### Specialty
    Player needs to seek out heat sources to prevent freezing to death
    Runes spawn more often
### Enemies
    Ice spirit, shoots freeze projectiles
    Shard golemn, explodes when killed, slow and high health, but low damage
    Glacial spider, hides in snow and shoots freeze projectiles and inflict frost on bites
    Yeti, mid speed, damage and health melee attack
    Frost warden, high defence and slow. Inflict slow in a radius around it
    Frost wolf, attacks in packs, weak individually, howls to attract others when one spots player
    Femir, wolf monsters with clubs. Medium damage and health, but high speed
    Shaman, summons blizzards
    Ice demon, boss, lowers temperature in area and causes player to freeze faster. High health and damage, but slow
    Leshy, boss, snares player with roots and shoots projectiles. Can teleport away when damage threshold is reached



# Biomes:
    Desert Biome, Water does not exist, enemies are vulnerable to fire, high gold in urns, 

    Mushroom Biom, poison effects are common, enemies here are immune to poision, more potion, exploding mushrooms, Mushroom Queen boss

    Crystal Caverns, High armour enemies, crystals that emit light, Rare gems

    Aztec Temple, dinosaurs worship, dinosaur skull masks for some enemies, 

    Lava forge, lots of lava, enemies are immune to fire and deal fire damage, rare weapons

    Ice Cave, Lots of ice, enemies are immune to freeze and deal freeze damage, breakable walls are more common

    Ancient ruins, undead enemies, rare runes

    Water caves, need to traverse lots of water, Deep water contains enemies, look for shallow water. More Treasure chests