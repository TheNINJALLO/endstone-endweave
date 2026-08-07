"""Protocol factory for v944 (r26_u1) server <- v975 (r26_u2) client."""

from functools import partial

from endstone_endweave.protocol import Protocol
from endstone_endweave.protocol.direction import Direction
from endstone_endweave.protocol.mappings.v944_v975 import MAPPINGS
from endstone_endweave.protocol.packet_ids import PacketId
from endstone_endweave.rewriter import SoundRewriter

from .handlers.actor_event import rewrite_actor_event
from .handlers.client_movement_prediction_sync import rewrite_client_movement_prediction_sync
from .handlers.crafting_data import rewrite_crafting_data
from .handlers.creative_content import rewrite_creative_content
from .handlers.inventory_content import rewrite_inventory_content
from .handlers.item_stack import (
    rewrite_inventory_slot,
    rewrite_mob_equipment,
)
from .handlers.level_sound_event import rewrite_level_sound_event
from .handlers.play_sound import rewrite_play_sound
from .handlers.start_game import rewrite_start_game
from .handlers.update_client_options import rewrite_update_client_options

SERVER_PROTOCOL = 944
CLIENT_PROTOCOL = 975


def create_protocol() -> Protocol:
    """Create a protocol for v944 server <- v975 client.

    Returns:
        A Protocol instance with all v944-to-v975 handlers registered.
    """
    p = Protocol(server_protocol=SERVER_PROTOCOL, client_protocol=CLIENT_PROTOCOL)

    sound = SoundRewriter(
        sound_remap=MAPPINGS.sound.shift_up,
        actor_data_int_remappers={MAPPINGS.actor_data_sound_key: MAPPINGS.sound.shift_up},
    )
    sound.register(p)
    p.register_clientbound(PacketId.LEVEL_SOUND_EVENT, rewrite_level_sound_event)
    p.register_clientbound(PacketId.START_GAME, rewrite_start_game)
    p.register_clientbound(PacketId.ACTOR_EVENT, partial(rewrite_actor_event, direction=Direction.CLIENTBOUND))
    p.register_clientbound(PacketId.PLAY_SOUND, rewrite_play_sound)
    p.register_clientbound(PacketId.INVENTORY_SLOT, rewrite_inventory_slot)
    p.register_clientbound(PacketId.INVENTORY_CONTENT, rewrite_inventory_content)
    p.register_clientbound(PacketId.CREATIVE_CONTENT, rewrite_creative_content)
    p.register_clientbound(PacketId.PLAYER_EQUIPMENT, partial(rewrite_mob_equipment, direction=Direction.CLIENTBOUND))
    p.register_clientbound(PacketId.CRAFTING_DATA, rewrite_crafting_data)

    p.register_serverbound(PacketId.PLAYER_EQUIPMENT, partial(rewrite_mob_equipment, direction=Direction.SERVERBOUND))
    p.register_serverbound(PacketId.UPDATE_CLIENT_OPTIONS, rewrite_update_client_options)
    p.register_serverbound(PacketId.CLIENT_MOVEMENT_PREDICTION_SYNC, rewrite_client_movement_prediction_sync)
    p.register_serverbound(PacketId.ACTOR_EVENT, partial(rewrite_actor_event, direction=Direction.SERVERBOUND))

    p.cancel_clientbound(
        PacketId.ADD_PLAYER,  # 46
        PacketId.ADD_ITEM_ACTOR,  # 15
        PacketId.MOB_ARMOR_EQUIPMENT,  # 32
        PacketId.LOCATOR_BAR,  # 341 -- TextureId(int) -> TexturePath(string) + IconSize(Vec2)
        PacketId.SERVER_SCRIPT_DEBUG_DRAWER,  # 328 -- ShapeDataPayload -> PrimitiveShapeDataPayload
        PacketId.CLIENTBOUND_ATTRIBUTE_LAYER_SYNC,  # 345 -- Weight switch removed
        PacketId.PLAYER_ENCHANT_OPTIONS,  # 146 -- ItemEnchantOption.Cost width changed
        PacketId.UPDATE_CLIENT_OPTIONS,
    )
    p.cancel_serverbound(
        PacketId.SERVERBOUND_DIAGNOSTICS,
        PacketId.PARTY_CHANGED,
    )

    return p
