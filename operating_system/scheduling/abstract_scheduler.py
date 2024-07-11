class AbtractSchedulerAlgorithm:
    def __init__(self, kernel, quantum):
        self.__kernel = kernel
        self.__quantum = quantum

    @property
    def kernel(self):
        """ Returns the OS kernel. """
        return self.__kernel

    @property
    def quantum(self):
        """ Returns the OS quantum or zero if none. """
        return self.__quantum

    @property
    def is_preemptive(self):
        """ Answers if this algorithm is preemptive or not. """
        raise RuntimeError("Should be implemented by the subclass, but it did not implement it.")

    @property
    def next_process_id(self):
        """ Returns the next process ID to execute. """
        raise RuntimeError("Should be implemented by the subclass, but it did not implement it.")

    def move_to_ready(self, pid, pcb):
        """ Move a process with the given pid and matching pcb to the ready state. """
        raise RuntimeError("Should be implemented by the subclass, but it did not implement it.")

    def move_to_running(self, pid, pcb):
        """ Move a process with the given pid and matching pcb to the running state. """
        raise RuntimeError("Should be implemented by the subclass, but it did not implement it.")

    def move_to_waiting(self, pid, pcb):
        """ Move a process with the given pid and matching pcb to the waiting state. """
        raise RuntimeError("Should be implemented by the subclass, but it did not implement it.")

    def __repr__(self):
        # The repr should return the processes ready in their corresponding order.
        pass