from utilities.printer import Printer
from utilities.queue import Queue

from operating_system.pcb import *

from operating_system.scheduling.non_preemptive.fcfs_scheduler import FCFSSchedulingAlgorithm
from operating_system.scheduling.non_preemptive.ljf_scheduler import LJFSchedulingAlgorithm
from operating_system.scheduling.non_preemptive.sjf_scheduler import SJFSchedulingAlgorithm
from operating_system.scheduling.preemptive.fpps_scheduler import FPPSSchedulingAlgorithm
from operating_system.scheduling.preemptive.lrtf_scheduler import LRTFSchedulingAlgorithm
from operating_system.scheduling.preemptive.srtf_scheduler import SRTFSchedulingAlgorithm
from operating_system.scheduling.preemptive.rr_scheduler import RRSchedulingAlgorithm
#from operating_system.scheduling.preemptive.mlq_scheduler import MLQSchedulingAlgorithm


""" It's useful to remember the following chart of states of a process
according to the different interruptions that may occur.

    NEW --                       --->TERMINATED
          |                      |
          |                      |
     #NEW |   ----------------   | #KILL
          |  |    #SWAP      |   |
          V  v               |   |
        READY -------------> RUNNING
          ^     #DISPATCH      |
  #IO_OUT |                    | #IO_IN
          |                    |
          ------  WAITING <-----
"""
class Scheduler():
    """
    Models the short-term scheduler in charge of performing the
    context switching and determine the next process to assign the CPU.
    For now we are going to follow a really simple strategy, based on
    a minimal queue.
    The Scheduler is the one in charge of maintaining which process is doing
    what, and changing them around in a coherent state at different times. It
    does this with support of the Dispatcher.
    """
    def __init__(self, kernel, scheduling_algorithm, quantum):
        self.__kernel = kernel
        # We create the list of possible algorithms to use.
        self.__available_scheduling_algorithms = {
            'FCFS': FCFSSchedulingAlgorithm(kernel, quantum),
            'LJF':  LJFSchedulingAlgorithm(kernel, quantum),
            'SJF':  SJFSchedulingAlgorithm(kernel, quantum),
            'FPPS': FPPSSchedulingAlgorithm(kernel, quantum),
            'SRTF': SRTFSchedulingAlgorithm(kernel, quantum),
            'LRTF': LRTFSchedulingAlgorithm(kernel, quantum),
            'RR':   RRSchedulingAlgorithm(kernel, quantum),
            #'MLQ':  MLQSchedulingAlgorithm(kernel, quantum)
        }
        # Then we keep track of the currently selected algorithm
        self.__current_algorithm_name = scheduling_algorithm
        self.__current_algorithm = self.__available_scheduling_algorithms[scheduling_algorithm]
        # Also, still we are going to keep track of the current process being
        # running by the CPU. The general scheduling is in charge of this,
        # while the algorithms define the next process to run.
        # Of course, we start with no process running.
        self.__currently_running_pid = None

    @property
    def current_algorithm_name(self):
        """ Returns the currently in use algorithm name. """
        return self.__current_algorithm_name

    @current_algorithm_name.setter
    def current_algorithm_name(self, value):
        """ Sets the current algorithm to the one with the given name. """
        if (value not in self.__available_scheduling_algorithms):
            raise RuntimeError("There is no scheduling algorithm by the name: " + value)
        self.__current_algorithm_name = value
        self.__current_algorithm = self.__available_scheduling_algorithms[value]

    @property
    def current_algorithm(self):
        """ Returns the currently in use algorithm. """
        return self.__current_algorithm

    @property
    def currently_running_pid(self):
        """ Returns the running process ID. """
        return self.__currently_running_pid

    @property
    def next_process_id(self):
        """
        Return the next process ID in the ready queue,
        if any, or None if there's no next process.
        Note that this does not remove the process
        from the queue.
        """
        # Just delegate to the algorithm in use
        return self.__current_algorithm.next_process_id

    ############### BASIC PROCESS STATE CHANGE ########################

    def move_to_ready(self, pid):
        """ Move a process with the given pid to the ready state. """
        # Get the associated PCB
        pcb = self.__kernel.process_table.get_pcb_by_pid(pid)
        # To become ready, the process may be in any state other than
        # terminated
        if pcb.state is TERMINATED:
            raise RuntimeError("IllegalState: A TERMINATED process cannot be moved to READY")
        # If it's already ready, it's a wrong request also
        if pcb.state is READY:
            raise RuntimeError("IllegalState: A READY process cannot be moved to READY")
        # If it's a new process, or if it comes from waiting there is not much to do in a general term.
        if pcb.state is NEW or pcb.state is WAITING:
            pass
        # If it is on the running state, we need to unload it from the CPU
        if pcb.state is RUNNING:
            self.__kernel.dispatcher.save(pcb)
            self.__currently_running_pid = None
        # Now that we have handled the basics, let's delegate to the
        # algorithm how to handle the passage of this process to ready
        # We do this before changing the state, so the algorithm can
        # count on where did the process came from
        self.__current_algorithm.move_to_ready(pid, pcb)
        # We always need to update the PCB to the ready state
        pcb.state = READY



    def move_to_running(self, pid):
        """ Move a process with the given pid to the running state. """
        # Get the associated PCB
        pcb = self.__kernel.process_table.get_pcb_by_pid(pid)
        # To become running, the process must be in the ready state
        if pcb.state is not READY:
            raise RuntimeError("IllegalState: A non READY process cannot be moved to RUNNING")
        # To become running, it must be the next process
        if pid is not self.next_process_id:
            raise RuntimeError("IllegalState: No process other than the next can be moved to running")
        # Set the process as the currently running one
        self.__currently_running_pid = pid
        # Change the PCB state to running
        pcb.state = RUNNING
        # Now let's delegate to the algorithm on how to move this process to running
        self.__current_algorithm.move_to_running(pid, pcb)
        # And load the PCB to the CPU
        self.__kernel.dispatcher.load(pcb)

    def move_to_waiting(self, pid):
        """ Move a process with the given pid to the waiting state. """
        # Get the associated PCB
        pcb = self.__kernel.process_table.get_pcb_by_pid(pid)
        # To become waiting, the process must be in the running state
        if pcb.state is not RUNNING:
            raise RuntimeError("IllegalState: A non RUNNING process cannot be moved to WAITING")
        # Save the CPU to the PCB
        self.__kernel.dispatcher.save(pcb)
        # Now, there is no running process (Another process should be moved
        # to running)
        self.__currently_running_pid = None
        # And of course, update the PCB state
        pcb.state = WAITING
        # Usually there is no much to do here, but some algorithms may require
        # to do something when a process has moved to waiting, so we need to
        # delegate to the algorithm
        self.__current_algorithm.move_to_waiting(pid, pcb)

    def move_to_terminated(self, pid):
        """ Move a process with the given pid to the terminated state. """
        # Get the associated PCB
        pcb = self.__kernel.process_table.get_pcb_by_pid(pid)
        # To become terminated, the process must be in the running state
        if not pcb.state == RUNNING:
            raise RuntimeError("IllegalState: A non RUNNING process cannot be moved to TERMINATED")
        # Save the CPU to the PCB
        self.__kernel.dispatcher.save(pcb)
        # Now, there is no running process (Another process should be moved
        # to running)
        self.__currently_running_pid = None
        # And of course, update the PCB state
        pcb.state = TERMINATED

    ############### END BASIC PROCESS STATE CHANGE ########################

    def __repr__(self):
        return Printer.tabulated([[
            Printer.tabulated([
                ["Currently running", self.__currently_running_pid],
                ["Ready queue", str(self.__current_algorithm)]
            ])]], headers=["Scheduler"]
        )