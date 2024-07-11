from utilities.printer import Printer

"""
Instructions used by the CPU.
Current implementation is just a string,
but they can be more complex entities if used properly.
"""
INSTRUCTION_IO = "IO"
INSTRUCTION_CPU = "CPU"
INSTRUCTION_EXIT = "EXIT"
# Used only to reflect the idea of a non-operation, that is, one not from the above
INSTRUCTION_NOOP = "NOOP"

class ASM:
    """ An utility class to create machine code programs. """
    @classmethod
    def EXIT(self):
        """ Return the EXIT instruction. """
        return INSTRUCTION_EXIT

    @classmethod
    def NOOP(self):
        """ Return the NOOP instruction. """
        return INSTRUCTION_NOOP

    @classmethod
    def IO(self, times=1):
        """ Return as many IO instructions as required. """
        return [INSTRUCTION_IO] * times

    @classmethod
    def CPU(self, times=1):
        """ Return as many CPU instructions as required. """
        return [INSTRUCTION_CPU] * times

    @classmethod
    def is_valid(self, instruction):
        """
        Answer if the given instruction is a valid one.
        NOOP is a special case and not consider valid.
        """
        return (
               self.is_CPU(instruction)
            or self.is_IO(instruction)
            or self.is_EXIT(instruction)
        )

    @classmethod
    def is_EXIT(self, instruction):
        """ Answer if the given instruction is the EXIT one. """
        return INSTRUCTION_EXIT == instruction

    @classmethod
    def is_NOOP(self, instruction):
        """ Answer if the given instruction is the NOOP one. """
        return INSTRUCTION_NOOP == instruction

    @classmethod
    def is_IO(self, instruction):
        """ Answer if the given instruction is an IO one. """
        return INSTRUCTION_IO == instruction

    @classmethod
    def is_CPU(self, instruction):
        """ Answer if the given instruction is a CPU one. """
        return INSTRUCTION_CPU == instruction

    @classmethod
    def _colored_instruction_(self, instruction):
        """ Returns the instruction colored for printing. Internal use only. """
        return ({
            INSTRUCTION_CPU: Printer.str_with_color(INSTRUCTION_CPU, Printer.GREEN),
            INSTRUCTION_IO: Printer.str_with_color(INSTRUCTION_IO, Printer.BLUE),
            INSTRUCTION_EXIT: Printer.str_with_color(INSTRUCTION_EXIT, Printer.RED),
            INSTRUCTION_NOOP: INSTRUCTION_NOOP # No color
        }[instruction])