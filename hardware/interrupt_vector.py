class InterruptVector():
    """
    Simulates the interruption vector.
    The interruption vector is a table that associates an interruption name/code,
    to a given handler. The vector allows to register new handlers for an
    interruption, and to handle such interruption by the associated handler
    when the interruption in thrown.
    """

    def __init__(self):
        """
        The handlers is an empty dictionary by default,
        it will get populated as handlers are registered.
        It never gets unpopulated, but associated handlers
        are called when the handle action is called.
        """
        self.__handlers = {}

    def register(self, irq_code, interruption_handler):
        """ Register a new interruption to the interruptor vector. """
        self.__handlers[irq_code] = interruption_handler

    def handle(self, irq):
        """ Handle an interruption with the registered handlers in the vector. """
        if irq.code in self.__handlers:
            self.__handlers[irq.code].execute(irq)
