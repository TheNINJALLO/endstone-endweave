from endstone_endweave.codec import ITEM_INSTANCE, ITEM_INSTANCE_V975, UVAR_INT, PacketWrapper


def rewrite_inventory_content(wrapper: PacketWrapper) -> None:
    """InventoryContentPacket (49): rewrite v944 layout into v975 layout.
    
    The packet structure is just ContainerID followed by an array of items.
    v944 uses the varint-based ITEM_INSTANCE, v975 uses the cerealized ITEM_INSTANCE_V975.
    """
    wrapper.passthrough(UVAR_INT)  # Container ID
    
    count = wrapper.read(UVAR_INT)
    wrapper.write(UVAR_INT, count)
    
    for _ in range(count):
        wrapper.map(ITEM_INSTANCE, ITEM_INSTANCE_V975)
