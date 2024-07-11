from utilities.printer import Printer

from hardware.hardware import HARDWARE

from operating_system.io_controller import IOController

class IOControllersVector:

    def __init__(self):
        self.__io_controllers = []
        for device_id in HARDWARE.io_devices_ids():
            self.__io_controllers.append(IOController(self, device_id))

    def get_by_id(self, device_id):
        """ Returns the IO controller for a given device id. """
        return self.__io_controllers[device_id]

    def __repr__(self):
        # We join the processes in a list of elements each, so
        # they are presented in two columns
        elements = []
        elements_added = 0
        columns = 3

        for e in self.__io_controllers:
            if (elements_added % columns == 0):
                elements.append([])
            elements[-1].append(e)
            elements_added += 1

        # Now we can use out list
        return Printer.tabulated(
            [[Printer.tabulated(elements, tablefmt="plain")]],
            headers=["IO Device Controllers"]
        )
