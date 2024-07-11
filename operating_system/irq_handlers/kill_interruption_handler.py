from hardware.hardware import HARDWARE
from hardware.irq import IRQ

from operating_system.irq_handlers.abstract_interruption_handler import AbstractInterruptionHandler

class KillInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        """ Kill the currently running process. """
        # We can get the PID of the current process running
        pid = self.kernel.scheduler.currently_running_pid
        # Then we move the process to terminated state
        self.kernel.scheduler.move_to_terminated(pid)
        # Now we can unload the process from memory and remove
        # it from the process table.
        self.kernel._kill_process(pid)
        # TODO: (3)
        # As the currently running process is now in terminated state,
        # the last step is to tell the scheduler to run the next process
        # in the ready queue, if any.
        HARDWARE.interrupt_vector.handle(IRQ.DISPATCH(self.kernel.scheduler.current_algorithm.is_preemptive))