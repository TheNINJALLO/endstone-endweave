from endstone_endweave.codec import NETWORK_ITEM_INSTANCE_DESCRIPTOR, ITEM_INSTANCE_V975, UVAR_INT, STRING, UINT_LE, PacketWrapper


def rewrite_creative_content(wrapper: PacketWrapper) -> None:
    """CreativeContentPacket (145): rewrite v944 layout into v975 layout.
    
    Layout:
    1. Groups array: Category (UINT_LE), Name (STRING), Icon (NETWORK_ITEM_INSTANCE_DESCRIPTOR)
    2. Items array: CreativeNetId (UVAR_INT), Item (NETWORK_ITEM_INSTANCE_DESCRIPTOR)
    """
    # 1. Groups Array
    groups_count = wrapper.read(UVAR_INT)
    wrapper.write(UVAR_INT, groups_count)
    
    for _ in range(groups_count):
        wrapper.passthrough(UINT_LE)  # Category
        wrapper.passthrough(STRING)  # Name
        wrapper.map(NETWORK_ITEM_INSTANCE_DESCRIPTOR, ITEM_INSTANCE_V975)  # Icon

    # 2. Items Array
    items_count = wrapper.read(UVAR_INT)
    wrapper.write(UVAR_INT, items_count)
    
    for _ in range(items_count):
        wrapper.passthrough(UVAR_INT)  # CreativeItemNetId
        wrapper.map(NETWORK_ITEM_INSTANCE_DESCRIPTOR, ITEM_INSTANCE_V975)  # Item
        wrapper.passthrough(UVAR_INT)  # Group ID

