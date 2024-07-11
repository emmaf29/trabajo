from hardware.hardware import HARDWARE
from hardware.irq import IRQ

from operating_system.irq_handlers.abstract_interruption_handler import AbstractInterruptionHandler

class NewInterruptionHandler(AbstractInterruptionHandler):

    def execute(self, irq):
        """
        Load a new program. That is, create a process for it, and
        set it a ready to run.
        """
        # The program is given as an argument of this IRQ.
        program = irq.arguments[0]
        # Perform the basic system calls
        pid = self.kernel._create_process(program)
        # The new state is quite transient. When a process is created
        # it should immediately be set to the READY state and put in
        # the ready queue. The scheduler is in charge of this.
        self.kernel.scheduler.move_to_ready(pid)
        # If there is no process running, most likely there is no
        # other process to execute, so move the next process to the
        # running state
        HARDWARE.interrupt_vector.handle(IRQ.DISPATCH(self.kernel.scheduler.current_algorithm.is_preemptive))
