from hardware.hardware import HARDWARE
from hardware.irq import IRQ

from operating_system.irq_handlers.abstract_interruption_handler import AbstractInterruptionHandler

class SwapInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        """
        Remove the currently running process and swap it for
        the next process in the ready state.
        """
        # TODO: (5)
        # We are handling preemption here. So we need to swap the
        # currently executing in the CPU, by the one next in the queue.
        # First, lets get the process running
        pid = self.kernel.scheduler.currently_running_pid
        # Now, let's move this process to ready state, as it can actually
        # still run, it's the OS who is telling it not to continue.
        self.kernel.scheduler.move_to_ready(pid)
        # Once in ready, we have to load the next process in the ready queue.
        # Not that, if there is only one process, it will be the same
        # process that we load.
        HARDWARE.interrupt_vector.handle(IRQ.DISPATCH(self.kernel.scheduler.current_algorithm.is_preemptive))
