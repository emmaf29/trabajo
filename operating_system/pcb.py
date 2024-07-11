from utilities.printer import Printer

from hardware.hardware import HARDWARE
from hardware.asm import ASM

NEW = "NEW"
READY = "READY"
WAITING = "WAITING"
RUNNING = "RUNNING"
TERMINATED = "TERMINATED"

class PCB:
    """Models a PCB"""

    def __init__(self, pid, memory_start, memory_size, priority = 3, category = 'batch'):
        self.__pid = pid
        self.__state = NEW
        self.__memory_start = memory_start
        self.__memory_size = memory_size
        self.__pc = 0
        #self.__pc = memory_start
        # For SJF, LJF, not used otherwise
        self.__burst_time = self.__calculate_burst_time(memory_start, memory_size)
        # For SRTF, LRTF, not used otherwise
        self.__remaining_time = self.__burst_time
        # For FPPS, not used otherwise
        self.__priority = priority
        # For MLQ, not used otherwise
        self.__category = category

    @property
    def pid(self):
        """ Returns the PCB's PID. """
        return self.__pid

    @property
    def state(self):
        """ Returns the PCB's state. """
        return self.__state

    @state.setter
    def state(self, value):
        """ Returns the PCB's state. """
        self.__state = value

    @property
    def memory_start(self):
        """
        Returns the initial memory position the
        associated program for this PCB is store at.
        """
        return self.__memory_start
    
    def memory_size(self):

        return self.memory_size

    @property
    def memory_end(self):
        """
        Returns the last memory position the
        associated program for this PCB is store at.
        """
        return self.memory_start + self.__memory_size

    @property
    def pc(self):
        """ Returns the status of the PC registry for this PCB. """
        return self.__pc

    @pc.setter
    def pc(self, value):
        """ Assign the status of the PC registry for this PCB. """
        self.__pc = value

    @property
    def burst_time(self):
        """ Returns the burst time of this PCB. """
        return self.__burst_time

    @property
    def priority(self):
        """ Returns the priority of this PCB. """
        return self.__priority

    @property
    def category(self):
        """ Returns the category of this PCB. """
        return self.__category

    @property
    def remaining_time(self):
        """ Returns the remaining time of this PCB. """
        return self.__remaining_time

    def recalculate_remaining_time(self):
        """ Recalculate and store the remaining time of this PCB. """
        self.__remaining_time = self.__calculate_burst_time(self.__pc, self.__memory_size)

    def __calculate_burst_time(self, from_addr, to_addr):
        """ Calculare the burst-time of the instruction from one memory position to the next"""
        cpu_instructions = [
            location
            for location in range(from_addr, to_addr)
            if ASM.is_CPU(HARDWARE.memory.read(location))
        ]
        return len(cpu_instructions)

    def __repr__(self):
        return Printer.tabulated([
            ["PID", self.__pid],
            ["State", self.__state],
            ["M.Start", self.__memory_start],
            ["M.Size", self.__memory_size],
            ["PC", self.__pc]
        ])
