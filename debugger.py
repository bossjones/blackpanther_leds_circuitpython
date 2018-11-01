import gc
import micropython  # pylint: disable=E0401
import sys


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
            print("obj.%s = %s" % (attr, getattr(obj, attr)))


def show_sizeof(x, level=0):
    # print("\t" * level, x.__class__, sys.getsizeof(x), x)
    print("{} {} {} {}".format(("\t" * level), x.__class__, sys.getsizeof(x), x))

    if hasattr(x, "__iter__"):
        if hasattr(x, "items"):
            for xx in x.items():
                show_sizeof(xx, level + 1)
        else:
            for xx in x:
                show_sizeof(xx, level + 1)


def get_obj_ref_count(foo):
    print(sys.getrefcount(foo))
