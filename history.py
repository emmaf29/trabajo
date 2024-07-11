from utilities.printer import Printer

from hardware.hardware import HARDWARE

class History:
    def __init__(self, os):
        self.__os = os
        self.__cpu_per_process_over_time = []
        self.__process_status_over_time = []
        self.__ticks_registered = 0
        self.__last_max_pid_seen = 0
        HARDWARE.clock.add_subscriber(self, 0)

    def tick(self, tick_number):
        # Register a new tick
        self.__ticks_registered += 1

        # Check if there is a new max process ID
        self.__last_max_pid_seen = self.__os.process_table.last_used_pid

        # Register the current process using the CPU at this tick
        pid = self.__os.scheduler.currently_running_pid
        self.__cpu_per_process_over_time.append(pid)

        # Register the status of all processes in existence for this tick
        self.__process_status_over_time.append([])
        for i in range(0, self.__last_max_pid_seen):
            if self.__os.process_table.has_pid(i+1):
                pcb = self.__os.process_table.get_pcb_by_pid(i+1)
                self.__process_status_over_time[-1].append(pcb.state)
            else:
                self.__process_status_over_time[-1].append('--')

    def to_string(self, columns = None):
        process_per_tick = []
        status_per_tick = []
        elements_added = 0
        columns = self.__ticks_registered if columns is None else columns

        for i in range(0, self.__ticks_registered):
            if (elements_added % columns == 0):
                process_per_tick.append([])
                status_per_tick.append([])

            e = self.__cpu_per_process_over_time[i]
            process_per_tick[-1].append((str(e) if e != None else 'IDLE', i))

            f = self.__process_status_over_time[i]
            status_per_tick[-1].append((f, i))

            elements_added += 1

        pprocess_per_tick = []
        if len(process_per_tick) > 0:
            for row in process_per_tick:
                pair = ([str(e) for (e, i) in row], ['Tick ' + str(i) for (e, i) in row])
                pair[0].insert(0, 'PID')
                pair[1].insert(0, '')
                pprocess_per_tick.append(pair)

        cpu_usage = "\n".join(
            [
                Printer.tabulated([row[0]],
                                  headers=row[1])
                for row in pprocess_per_tick
            ]
        )

        # Convert columns in status_per_tick to rows
        # First add as many rows as processes
        pstatus_per_ticks = []
        if len(status_per_tick) > 0:
            for row in status_per_tick:
                rows = []
                for i in range(0, self.__last_max_pid_seen):
                    rows.append([i+1])
                for t in range(0, len(row)):
                    for i in range(0, self.__last_max_pid_seen):
                        rows[i].append(row[t][0][i] if len(row[t][0]) > i else '--')
                pair = (rows, ['Tick ' + str(i) for (e, i) in row])
                pair[1].insert(0, 'PID')
                pstatus_per_ticks.append(pair)

        process_status = "\n".join(
            [
                Printer.tabulated(row[0],
                                  headers=row[1])
                for row in pstatus_per_ticks
            ]
        )

        # Now we can use out list
        return Printer.tabulated([[cpu_usage]],
            headers=["Process in execution on the CPU over time"]
        ) + "\n\n" + Printer.tabulated([[process_status]],
            headers=["Process status over time"]
        )

    def __repr__(self):
        return self.to_string(8)