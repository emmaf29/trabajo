from utilities.printer import Printer

class ProcessTable():
    """
    Models the process table. The same as a dictionary,
    but we can add additional data, such as which is the next process ID.
    Besides, we can talk about the domain, such as, all_process_ids, instead
    of just asking for the keys.
    """
    def __init__(self):
        """ Create a process table. """
        self.__table = {}
        self.__last_used_pid = 0

    @property
    def last_used_pid(self):
        """ Return the last used pid. Should be uses only for printing history. """
        return self.__last_used_pid

    def get_next_pid(self):
        """
        Increment the last used PID and return it.
        Every access returns a different number.
        """
        self.__last_used_pid += 1
        return self.__last_used_pid

    def has_pid(self, pid):
        """ Answers if a process ID is present in the table. """
        return pid in self.__table

    def get_pcb_by_pid(self, pid):
        """ Return a PCB for the process ID. """
        return self.__table[pid]

    def add_new_pcb(self, pcb):
        """ Add a new PCB to the table. """
        self.__table[pcb.pid] = pcb

    def remove_pcb(self, pcb):
        """ Remove a PCB from the table. """
        del self.__table[pcb.pid]

    def number_of_processes(self):
        """ Return the number of processes. """
        return len(self.__table)

    def all_pids(self):
        """ Return all the processes ids. """
        return self.__table.keys()

    def all_pcbs(self):
        """ Return all the PCBs. """
        return self.__table.items()

    def __repr__(self):
        # We join the processes in a list of elements each, so
        # they are presented in two columns
        elements = []
        elements_added = 0
        columns = 3

        for _, pcb in self.__table.items():
            if (elements_added % columns == 0):
                elements.append([])
            elements[-1].append(pcb)
            elements_added += 1

        # Now we can use out list
        return Printer.tabulated(
            [[Printer.tabulated(elements, tablefmt="plain")]],
            headers=["Process Table"]
        )