from utilities.printer import Printer

from hardware.hardware import HARDWARE
from hardware.irq import *

from operating_system.pcb import PCB
from operating_system.process_table import ProcessTable
from operating_system.loader import Loader
from operating_system.scheduler import Scheduler
from operating_system.dispatcher import Dispatcher
from operating_system.io_controllers_vector import IOControllersVector
from operating_system.irq_handlers.kill_interruption_handler import KillInterruptionHandler
from operating_system.irq_handlers.new_interruption_handler import NewInterruptionHandler
from operating_system.irq_handlers.io_in_interruption_handler import IoInInterruptionHandler
from operating_system.irq_handlers.io_out_interruption_handler import IoOutInterruptionHandler
from operating_system.irq_handlers.swap_interruption_handler import SwapInterruptionHandler
from operating_system.irq_handlers.dispatch_interruption_handler import DispatchInterruptionHandler

class Kernel:
    """ Models the kernel of the OS. """

    def __init__(self, scheduling_strategy = 'FCFS', quantum = 0):
        # The process table holds all the PCB's, it contains information
        # of all the processes currently alive in the system. It also holds
        # other additional behavior, such as answering which is the next PID.
        self.__process_table = ProcessTable()
        # The Loader is in charge of loading new processes into memory. We are
        # going to use the Loader instead of a long term scheduler, as LTSs
        # should perform heuristics to determine if it's a good time or not
        # to add a process, and when it should be added. Instead, we are going
        # to pursue a simpler approach. Our LTS was currently only a loader.
        self.__loader = Loader(self)
        # The Dispatcher is the part of the OS in charge of switching the
        # context of the CPU from one process to the next. It does not
        # control which process to load, but jut loads and unloads a process.
        self.__dispatcher = Dispatcher(self)
        # The Scheduler, as in, the Short-Term Scheduler, is going to be in
        # charge of assigning CPU usage to a particular process in time.
        # It's going to keep track of which PID is currently being
        # executed, which processes are waiting for execution, which are waiting
        # for IO to finish, and so on. It's in charge of performing the
        # context_switch.
        self.__scheduler = Scheduler(self, scheduling_strategy, quantum)
        # The IO controllers are the ones that handle the request to each
        # IO device. There is one for each device. The IO controllers vector
        # is the one in charge of retrieving the right controller for a given
        # device id. Although not strictly a part of the OS, this is really
        # convenient for managing and printing.
        self.__io_controllers_vector = IOControllersVector()



        # The OS should register a handler for each type of interruption
        # the hardware defines. How to handle the interruptions is up to the
        # operating system.
        HARDWARE.interrupt_vector.register(NEW_IRQ, NewInterruptionHandler(self))
        HARDWARE.interrupt_vector.register(KILL_IRQ, KillInterruptionHandler(self))
        # TODO: (3)
        # We need to add a handler for each interruption type. Note
        # that some handlers are not yet finished, so you may need to
        # add them in the extent that you finish them.
        HARDWARE.interrupt_vector.register(IO_IN_IRQ, IoInInterruptionHandler(self))
        HARDWARE.interrupt_vector.register(IO_OUT_IRQ, IoOutInterruptionHandler(self))
        HARDWARE.interrupt_vector.register(SWAP_IRQ, SwapInterruptionHandler(self))
        HARDWARE.interrupt_vector.register(DISPATCH_IRQ, DispatchInterruptionHandler(self))


    @property
    def process_table(self):
        """ Returns the process table of the OS. """
        return self.__process_table

    @property
    def loader(self):
        """ Returns the loader. """
        return self.__loader

    @property
    def dispatcher(self):
        """ Returns the dispatcher. """
        return self.__dispatcher

    @property
    def scheduler(self):
        """ Returns the scheduler. """
        return self.__scheduler

    @property
    def io_controllers_vector(self):
        """ Returns the IO controllers vector. """
        return self.__io_controllers_vector

    ############### SYSTEM CALLS ########################

    # This functions represent the system calls, that is, operations
    # that user programs (or the user through a shell) can call in order
    # to ask the OS for some action to be performed. Among some, are
    # creating processes, killing processes, etc. Not every system call
    # of a real OS is represented here, as we only provide some simple
    # examples. There are more high level system calls, and more low level.

    ###### High level:

    def load_program(self, program):
        """
        Load a new program. That is, create a process for it, and
        set it a ready to run. We achieve this through the use of
        an IRQ.
        """
        # We achieve this through an IRQ
        HARDWARE.interrupt_vector.handle(IRQ.NEW(program))

    ###### Low level (Should not be called from Main, but only from the OS):

    def _create_process(self, program):
        """
        Create a new process with the associated given program.
        Return the created process PID.
        """
        mem_start = self.__loader.load(program.instructions)
        pcb = PCB(self.__process_table.get_next_pid(), mem_start, len(program.instructions))
        self.__process_table.add_new_pcb(pcb)
        return pcb.pid

    def _kill_process(self, pid):
        """ Kill the process with the given process ID. """
        pcb = self.__process_table.get_pcb_by_pid(pid)
        self.__loader.unload(pcb)
        self.__process_table.remove_pcb(pcb)

    ############### END SYSTEM CALLS ########################

    def __repr__(self):
        os_config = Printer.tabulated([[
            Printer.tabulated([
                ["Sch. Algorithm", self.__scheduler.current_algorithm_name],
                ["Quantum", self.__scheduler.current_algorithm.quantum]
            ])
        ]], headers=["Configuration"])

        return "\n".join([
            os_config,
            str(self.__scheduler),
            str(self.__io_controllers_vector),
            str(self.__process_table)
        ])
