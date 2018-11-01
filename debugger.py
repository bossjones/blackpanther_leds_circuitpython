import gc
import micropython  # pylint: disable=E0401
gc.collect()

def memorySnapshot(location=None):
    print("\n------memorySnapshot-----")
    if location:
        print("Location: {}\n".format(location))

    # pylint: disable=E1101
    print("Free memory: {} bytes".format(gc.mem_free()))  # pylint: disable=E1101
    print("Allocated memory: {} bytes".format(gc.mem_alloc()))  # pylint: disable=E1101
    print("Stack Use: {}".format(micropython.stack_use()))  # pylint: disable=E1101
    print("Memory Info:")  # pylint: disable=E1101
    print("-----------------------------")
    micropython.mem_info(1)
    print("-----------------------------")
    print("\n")

def dump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("obj.{} = {}".format(attr, getattr(obj, attr)))
