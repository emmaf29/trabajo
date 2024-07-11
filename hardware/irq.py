"""
The computer's supported interruption codes.
Typically this will be numbers, but using strings make it simpler
for our implementation.
"""

KILL_IRQ = "#KILL"
NEW_IRQ = "#NEW"
IO_IN_IRQ = "#IO_IN"
IO_OUT_IRQ = "#IO_OUT"
SWAP_IRQ = "#SWAP"
DISPATCH_IRQ = "#DISPATCH"

class IRQ:
    """ Models an Interruption, with it's code and arguments. """

    @classmethod
    def KILL(self):
        """ Return an interruption for the KILL code. """
        return IRQ(KILL_IRQ, [])

    @classmethod
    def NEW(self, program, priority=0):
        """ Return an interruption for the NEW code. """
        return IRQ(NEW_IRQ, [program, priority])

    @classmethod
    def IO_IN(self, device):
        """ Return an interruption for the IO_IN code for the given device. """
        return IRQ(IO_IN_IRQ, [device])

    @classmethod
    def IO_OUT(self, device):
        """ Return an interruption for the IO_OUT code for the given device. """
        return IRQ(IO_OUT_IRQ, [device])

    @classmethod
    def SWAP(self):
        """ Return an interruption for the SWAP code. """
        return IRQ(SWAP_IRQ, [])

    @classmethod
    def DISPATCH(self, preemptive = True):
        """ Return an interruption for the DISPATCH code. """
        return IRQ(DISPATCH_IRQ, [preemptive])

    def __init__(self, code, arguments = []):
        """ Create a new interruption. """
        self.__code = code
        self.__arguments = arguments

    @property
    def code(self):
        """ Return the code of this interruption. """
        return self.__code

    @property
    def arguments(self):
        """ Return the arguments of this interruption. """
        return self.__arguments