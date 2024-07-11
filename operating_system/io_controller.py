from utilities.printer import Printer
from utilities.queue import Queue

from hardware.hardware import HARDWARE

class IOController:
    """
    The IO Controller class is in charge of managing an IO device, dispatching
    requests to the device, and handling the request finalization (after an IRQ
    has called it).
    It handles the request queues, so only one request is sent at a time to a
    given device. Once a request finishes, it sends the next request, or does
    nothing if there are no more requests. There is one IOController per device.
    """

    def __init__(self, kernel, io_device_id):
        self.__kernel = kernel
        self.__io_device_id = io_device_id
        self.__currently_running_pid = None
        self.__request_queue = Queue()

    def active_pid(self):
        """
        Return the process id of the process currently
        sending a request to the device.
        If no request has been sent, returns None.
        """
        return self.__currently_running_pid

    def request(self, pid):
        """
        Add a request to the IO device from the given process
        ID to the queue.
        """
        self.__request_queue.enqueue(pid)
        self.__send_next_request__()

    def finish(self):
        """
        Finish the current request of the IO device,
        sending the next one, if any.
        """
        self.__currently_running_pid = None
        self.__send_next_request__()

    def __send_next_request__(self):
        device = HARDWARE.io_device(self.__io_device_id)
        if (not self.__request_queue.is_empty and device.is_idle):
            self.__currently_running_pid = self.__request_queue.dequeue()
            device.request()

    def __repr__(self):
        return Printer.tabulated([
            ["IO Device", self.__io_device_id],
            ["Currently running", self.__currently_running_pid],
            ["Request queue", str(self.__request_queue)]
        ])