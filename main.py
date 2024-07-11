#!/usr/bin/env python3
import traceback
from cmd import Cmd

from history import History

from utilities.printer import Printer
from utilities.compiler import Compiler

from hardware.hardware import HARDWARE

from operating_system.kernel import Kernel

class HardwareManagementCLIApp(Cmd):

    ############### HARDWARE CONFIGURATION AND BEHAVIOR ########################
    _memory_size=30
    _clock_speed=1  
    _io_device_timings=[1, 2]
    ############### END HARDWARE CONFIGURATION AND BEHAVIOR ########################

    ############### OS CONFIGURATION AND BEHAVIOR ########################
    #### ESTO LO ESTAMOS CAMBIANDO, ERA FCFS 
    _scheduler_algorithm='FCFS'
    _quantum=0
    ############### END OS CONFIGURATION AND BEHAVIOR ########################

    ############### MANAGER CONFIGURATION AND BEHAVIOR ########################
    _showing_ticks = False
    _start_in_turbo_mode=True
    # Automatically run tests at startup
    _automatically_run__tests=[1]
    # If none, print to console, else, print the
    # output to a file
    _history_output_file='out.txt'
    ############### END MANAGER CONFIGURATION AND BEHAVIOR ########################

    ############### CLI APP CONFIGURATION ########################

    prompt = "Hardware >> "
    intro = "Welcome to the hardware manager. Type 'help' for available commands."
    os = None
    history = None

    def preloop(self):
        """
        This method is executed before starting the application,
        so it"s used to initialize all elements.
        """

        # Initialize the Printer
        Printer.initialize()

        # Initialize the hardware
        HARDWARE.setup(
            memory_size=self._memory_size,
            clock_speed=self._clock_speed,
            device_timings= self._io_device_timings
        )

        # Initialize the Operating System
        self.os = Kernel(scheduling_strategy=self._scheduler_algorithm, quantum=self._quantum)

        # The history helps us in visualizing how the
        # execution happened, is not part of the hardware nor
        # the os, but just a mean to print data over time
        self.history = History(self.os)

        # We subscribe, in order to print after every tick the
        # hardware status.
        HARDWARE.clock.add_subscriber(self)

        # Adjust speed if starting in turbo mode
        if (self._start_in_turbo_mode):
            HARDWARE.clock.overclock()
        for test in self._automatically_run__tests:
            self.__class__.__dict__['test_' + str(test)].__call__(self)

    def test_1(self):
        self.do_load('cpu_long')
        self.do_tick(4)
        self.do_load('cpu_short')
        self.do_tick(1)
        self.do_load('cpu_medium')
        self.do_tick(4)
        self.do_load('cpu_short')
        self.do_tick(25)
        self.do_history()

    def test_2(self):
        self.do_load('p1', 2)
        self.do_tick(2)
        self.do_load('p2', 3)
        self.do_tick(2)
        self.do_load('p3', 3)
        self.do_tick(2)
        self.do_load('p4', 4)
        self.do_tick(2)
        self.do_load('p5', 1)
        self.do_tick(12)
        self.do_history()

    def do_quit(self, line = None):
        """ Exit the application. """
        return True

    ############### END CLI APP CONFIGURATION ########################

    ############### MANIPULATE HARDWARE ########################

    def do_on(self, line = None):
        """ Turn ON the computer. """
        Printer.show(" ---- TURNING COMPUTER ON ---- ")
        HARDWARE.turn_on()

    def do_off(self, line = None):
        """ Turn OFF the computer. """
        HARDWARE.turn_off()
        Printer.show(" ---- TURNING COMPUTER OFF ---- ")

    def do_turbo_on(self, line = None):
        """ Turn ON turbo mode. """
        # Turbo sets the speed of the clock to immediate mode,
        # this is usefull when running ticks manually for debugging
        HARDWARE.clock.overclock()
        Printer.show(" ---- STARTING TURBO MODE ---- ")

    def do_turbo_off(self, line = None):
        """ Turn OFF turbo mode. """
        # Set the speed back to original value
        HARDWARE.clock.reset()
        Printer.show(" ---- ENDING TURBO MODE ---- ")

    def do_status(self, line = None):
        """ Show the hardware status. """
        data = Printer.tabulated([[HARDWARE, self.os]],
            headers=["Hardware", "Operating System"],
            numalign="center", stralign="left"
        )
        Printer.show(data)

    def do_history(self, line = None):
        """ Show the hardware status. """
        if self._history_output_file is None:
            Printer.show(self.history)
        else:
            f = open(self._history_output_file, 'w', encoding='utf-8')
            f.write(self.history.to_string())
            f.close()

    ############### END MANIPULATE HARDWARE ########################


    ############### SIMULATE TICKING ########################

    def do_tick(self, line = 1):
        """
        Run a clock"s tick, even if computer is off.
        Useful for debugging only.
        """
        ticks = 1

        if (type(line) == str and line != "" and line.isdigit()):
            ticks = int(line)
        elif (type(line) == int):
            ticks = line

        for _ in range(ticks):
            HARDWARE.clock.tick()

    def do_show_ticks(self, line = None):
        """ Show the hardware status. """
        self._showing_ticks = True

    def do_hide_ticks(self, line = None):
        """ Show the hardware status. """
        self._showing_ticks = False

    def tick(self, tick_number):
        """
        React to a tick of the clock.
        Only useful to print the status in each tick
        and see in real time what changes.
        """
        if (self._showing_ticks):
            Printer.show("        --------------- tick: {tick_number} ---------------".format(tick_number = tick_number))
            self.do_status("")

    ############### END SIMULATE TICKING ########################


    ############### LOAD PROGRAMS ########################

    def do_load(self, line = None):
        """ Load a program from the ones in the programs folder. """
        try:
            # Get the filename
            filename : str = line.strip()
            if not filename.endswith('.asm'):
                filename += '.asm'
            # Open a file with such name from the programs folder
            file_handle = open('./programs/' + filename)
            # Read the contents, removing extra spaces and empty lines or comments
            contents = [line.strip() for line in file_handle.readlines()
                        if line.strip() != "" and not line.strip().startswith("#")]
            #
            program = Compiler.compile(filename, contents)
            self.os.load_program(program)
        except FileNotFoundError:
            Printer.error("No program with the name: " + line + "in the ./programs folder.")
        except SyntaxError:
            Printer.error("The program " + line + " contains invalid ASM commands.")
        except Exception as e:
            Printer.error("ERROR: " + str(e))
            Printer.error(traceback.format_exc())

    def do_kill(self, line = None):
        """ Kill the process with given PID. """
        try:
            pid = int(line.strip())
            self.os.kill_process(pid)
        except ValueError:
            Printer.error(line + " is not a valid number for a process id.")
        except Exception as e:
            Printer.error("ERROR: " + str(e))
            Printer.error(traceback.format_exc())

    ############### END LOAD PROGRAMS ########################

if __name__ == "__main__":
    HardwareManagementCLIApp().cmdloop()
