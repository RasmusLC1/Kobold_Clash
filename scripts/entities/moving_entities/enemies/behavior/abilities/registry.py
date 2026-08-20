# Global registry dictionary
ABILITY_REGISTRY = {}

def register_ability(key):
    def decorator(cls): # cls = Classmethods
        ABILITY_REGISTRY[key] = cls
        return cls
    
    return decorator



from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.movement.dash import Dash
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.movement.jump_attack import Jump_Attack
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.movement.run_away import Run_Away
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.effects.invulnerable import Invulnerable
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.effects.invisibility import Invisibility
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.effects.rage import Rage
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.movement.charge import Charge
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.support_nearby_enemies.rally import Rally
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.support_nearby_enemies.electrify import Electrify
from scripts.entities.moving_entities.enemies.behavior.abilities.active_ability.support_nearby_enemies.healer import Healer
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.crystal_scale import Crystal_Scale
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.explode_on_impact import Explode_On_Impact
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.gloom_stalker import Gloom_Stalker
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.bone_seeker.bone_eater import Bone_Eater
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.bone_seeker.bone_ressurector import Bone_Resurrector
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.damage_reduction.ethereal import Ethereal
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.damage_reduction.anti_magic import Anti_Magic
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.healing.fire_born import Fire_Born
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.healing.glacial_core import Glacial_Core
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.healing.adaptability import Adaptability
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.healing.toxicosis import Toxicosis
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.healing.galvanic_skin import Galvanic_Skin
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.healing.sanguine_lord import Sanguine_Lord
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.clatter.echo_location import Echo_Location
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.clatter.echo_shard import Echo_Shard
from scripts.entities.moving_entities.enemies.behavior.abilities.passive_ability.clatter.echo_teleport import Echo_Teleport
