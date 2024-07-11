from utilities.printer import Printer

from hardware.memory import Memory
from hardware.mmu import MMU
from hardware.cpu import Cpu
from hardware.io_device import IODevice
from hardware.clock import Clock
from hardware.interrupt_vector import InterruptVector

class Hardware():
    """
    Represents a full computer hardware, the "motherboard" along with the
    other components wired in, if you may.
    """

    def setup(self, memory_size = 20, clock_speed = 1, device_timings = []):
        self.__memory = Memory(memory_size)
        self.__mmu = MMU(self.__memory)

        self.__interrupt_vector = InterruptVector()

        self.__io_devices = []
        for i in range(0, len(device_timings)):
            self.__io_devices.append(IODevice(i, device_timings[i], self.__interrupt_vector))

        self.__cpu = Cpu(self.__mmu, self.__interrupt_vector, len(self.__io_devices))

        self.__clock = Clock(clock_speed)
        # The order in which the elements are added to the clock
        # is important, the CPU needs to be added first, as
        # some instructions may activate actions. This behavior
        # is taken into account in the IO devices.
        self.__clock.add_subscriber(self.__cpu, 30)
        for io in self.__io_devices:
            self.__clock.add_subscriber(io, 15)

    @property
    def cpu(self):
        """ Returns the hardware's CPU. """
        return self.__cpu

    @property
    def memory(self):
        """ Returns the hardware's memory. """
        return self.__memory

    @property
    def mmu(self):
        """ Returns the hardware's mmu. """
        return self.__mmu

    @property
    def io_devices(self):
        """ Return a list of all IO devices. """
        return self.__io_devices

    @property
    def interrupt_vector(self):
        """ Returns the interruption vector. """
        return self.__interrupt_vector

    @property
    def clock(self):
        """ Returns the hardware's clock. """
        return self.__clock

    def io_devices_ids(self):
        """ Return the list of all the ids of IO devices. """
        return [device.device_id for device in self.__io_devices]

    def io_device(self, io_device_id):
        """ Return the IO device with the given id. """
        return self.__io_devices[io_device_id]

    def turn_on(self):
        """ Start the hardware's clock. """
        self.__clock.start()

    def turn_off(self):
        """ Stop the hardware's clock. """
        self.__clock.stop()

    def __repr__(self):
        cpu_panel = Printer.tabulated([[
            self.__cpu
        ]], headers=["CPU"], numalign="center", stralign="left")

        io_devices_panel = Printer.tabulated([[
            "\n".join([str(d) for d in self.__io_devices]),
        ]], headers=["IO Devices"], numalign="center", stralign="left")

        memory_panel = Printer.tabulated([[
            self.__memory,
        ]], headers=["Memory"], numalign="center", stralign="left")

        return Printer.tabulated([[
                cpu_panel + "\n" + io_devices_panel,
                memory_panel
            ]],
            tablefmt="plain"
        )


"""An instance of the hardware that acts as a global variable
being accessible from anywhere"""
HARDWARE = Hardware()