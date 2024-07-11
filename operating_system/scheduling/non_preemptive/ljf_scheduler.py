from utilities.priority_queue import PriorityQueue
from operating_system.scheduling.non_preemptive.non_preemptive_scheduler import NonPreemptiveSchedulerAlgorithm
class LJFSchedulingAlgorithm(NonPreemptiveSchedulerAlgorithm):
    """ Implementation of Longest Job First Scheduling Algorithm. """

    # TODO (2) Complete the class

    def __init__(self, kernel, quantum):
        super().__init__(kernel, quantum)
        self.__ready_queue = PriorityQueue()
        

    @property
    def next_process_id(self):
        self.__ready_queue.front

    
    def move_to_ready(self, pid, pcb):
        self.__ready_queue.enqueue(pid, -pcb.burst.time)

    
    
    def move_to_running(self, pid, pcb):
        self.__ready_queue.dequeue()



    def move_to_waiting(self, pid, pcb):
        pass

    def __repr__(self):
        return str(self.__ready_queue)