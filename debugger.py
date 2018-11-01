import gc
import micropython  # pylint: disable=E0401
import sys
import traceback

def memorySnapshot(location=None):
    print("\n------memorySnapshot-----")
    if location:
        print("Location: {}\n".format(location))

    # pylint: disable=E1101
    print("Free memory: {} bytes".format(gc.mem_free())
          )  # pylint: disable=E1101
    print("Allocated memory: {} bytes".format(gc.mem_alloc())
          )  # pylint: disable=E1101
    print("Stack Use: {}".format(micropython.stack_use())
          )  # pylint: disable=E1101
    print("Memory Info:")  # pylint: disable=E1101
    print('-----------------------------')
    micropython.mem_info(1)
    print('-----------------------------')
    print("\n")


def dump(obj):
    for attr in dir(obj):
        if hasattr(obj, attr):
            print("obj.%s = %s" % (attr, getattr(obj, attr)))


def show_sizeof(x, level=0):
    # print("\t" * level, x.__class__, sys.getsizeof(x), x)
    print("{} {} {} {}".format(("\t" * level), x.__class__, sys.getsizeof(x), x))

    if hasattr(x, '__iter__'):
        if hasattr(x, 'items'):
            for xx in x.items():
                show_sizeof(xx, level + 1)
        else:
            for xx in x:
                show_sizeof(xx, level + 1)

def get_obj_ref_count(foo):
    print(sys.getrefcount(foo))


def log_exception(exception: BaseException, expected: bool = True):
    """Prints the passed BaseException to the console, including traceback.

    :param exception: The BaseException to output.
    :param expected: Determines if BaseException was expected.
    """
    output = "[{}] {}: {}".format(
        'EXPECTED' if expected else 'UNEXPECTED', type(exception).__name__, exception)
    print(output)
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_tb(exc_traceback)
