from utilities.printer import Printer

from hardware.irq import IRQ

class IODevice:
    """ Models an IO device. """

    def __init__(self, device_id, operation_time, interrupt_vector):
        self.__device_id = device_id
        self.__operation_time = operation_time
        self.__is_busy = False
        self.__current_request_steps = -1
        self.__interrupt_vector = interrupt_vector

    @property
    def device_id(self):
        """ Returns this device ID. """
        return self.__device_id

    @property
    def operation_time(self):
        """ Returns the time it takes this device to answer a request. """
        return self.__operation_time

    @property
    def is_busy(self):
        """ Answers if this device is busy. """
        return self.__is_busy

    @property
    def is_idle(self):
        """ Answers if this device is idle. """
        return not self.__is_busy

    def request(self):
        """ Perform a request to this device. """
        if (self.__is_busy):
            raise RuntimeError("The IO device is busy, cannot receive requests")
        self.__is_busy = True

    def tick(self, tick_number):
        """
        Responds to a tick of the clock by advancing the time
        of processing a request.
        """
        if (self.__is_busy):
            self.__current_request_steps += 1
        if (self.__current_request_steps >= self.__operation_time):
            self.__is_busy = False
            self.__current_request_steps = -1
            self.__interrupt_vector.handle(IRQ.IO_OUT(self.__device_id))

    def __repr__(self):
        return Printer.tabulated([
            ["ID", self.__device_id],
            ["Op. Time", self.__operation_time],
            ["Status", "BUSY" if self.__is_busy else "IDLE"]
        ])