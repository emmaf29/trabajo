class AbstractInterruptionHandler():
    """
        Models an abstract interruption handler.
        A handler has access to the kernel, and knows how
        to "execute" on an IRQ.
    """

    def __init__(self, kernel):
        self._kernel = kernel

    @property
    def kernel(self):
        return self._kernel

    def execute(self, irq):
        raise RuntimeError("SUBCLASS RESPONSIBILITY: -- EXECUTE MUST BE OVERWRITTEN in class {classname}".format(classname=self.__class__.__name__))

