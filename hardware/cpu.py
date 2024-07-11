from random import randint

from utilities.printer import Printer

from hardware.asm import ASM
from hardware.irq import IRQ

class Cpu():
    """ Models the hardware"s CPU. """

    def __init__(self, mmu, interrupt_vector, number_of_io_devices):
        """
        The mmu and interruption vectors should be known by the CPU.
        Additionally, the number of IO devices should be known, as the be
        able to access a device randomly.
        """
        # Other hardware components
        self.__mmu = mmu
        self.__interrupt_vector = interrupt_vector
        self.__number_of_io_devices = number_of_io_devices
        # Registries
        self.__pc = -1
        self.__ir = ASM.NOOP()

    @property
    def pc(self):
        """Access the PC registry value"""
        return self.__pc

    @pc.setter
    def pc(self, addr):
        """Set the PC registry value"""
        self.__pc = addr

    @property
    def ir(self):
        """Access the IR registry value"""
        return self.__ir

    @property
    def is_busy(self):
        """Answers if the CPU is busy. If the PC is not -1, is busy"""
        return self.__pc >= 0

    @property
    def is_idle(self):
        """Answers if the CPU is idle. If the PC is -1, is idle"""
        return self.__pc == -1

    def tick(self, tick_number):
        """Emulate a tick of the clock, performing the FDE cycle"""
        # Remember lat tick for printing purposes
        self.__last_tick = tick_number-1
        # If the CPU is idle, no action is performed
        if (self.is_idle):
            self.__show_instruction(ASM.NOOP())
        else:
            # Perform FDE cycle
            self.__fetch()
            self.__decode()
            self.__execute()

    def __fetch(self):
        """Perform the Fetch part of a FDE cycle."""
        self.__ir =  self.__mmu.fetch(self.__pc) or ASM.NOOP()
        self.__pc = self.__pc + 1

    def __decode(self):
        """Perform the Decode part of a FDE cycle."""
        # Current implementation does not do anything at the moment
        pass

    def __execute(self):
        """Perform the Execute part of a FDE cycle."""
        # Any action should pass through __execute_any
        self.__execute_any()
        # Now, execute differently according to the actual instruction
        # to be executed. We delegate the task to another method.
        if ASM.is_CPU(self.__ir):
            self.__execute_cpu()
        if ASM.is_IO(self.__ir):
            self.__execute_io()
        if ASM.is_EXIT(self.__ir):
            self.__execute_exit()

    def __execute_any(self):
        """
        Every instruction is executed in this way, which involves printing
        the instruction to the screen.
        """
        self.__show_instruction(self.__ir)

    def __execute_cpu(self):
        """
        The CPU instructions are executed in this way.
        Currently, nothing is there to do.
        """
        pass

    def __execute_io(self):
        """
        The IO instructions are executed in this way.
        An IO_IN interruption should be handled by the interruption vector
        """
        random_dev_id = randint(0, self.__number_of_io_devices-1)
        self.__interrupt_vector.handle(IRQ.IO_IN(random_dev_id))

    def __execute_exit(self):
        """
        The EXIT instructions are executed in this way.
        A KILL interruption should be handled by the interruption vector
        """
        self.__interrupt_vector.handle(IRQ.KILL())

    def __show_instruction(self, instruction):
        """Print an instruction to the screen"""
        Printer.show("Executing instruction: {instr}".format(instr=ASM._colored_instruction_(instruction)))

    def __repr__(self):
        return Printer.tabulated([
            ["PC", self.__pc],
            ["IR", self.__ir],
            ["Base", self.__mmu.baseDir],
            ["Limit", self.__mmu.limit]
        ])
