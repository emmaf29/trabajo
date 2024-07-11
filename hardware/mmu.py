class MMU():
    """
    Emulates the behavior of a Memory Management Unit,
    translating from virtual memory to physical memory
    """

    def __init__(self, memory):
        self.__memory = memory
        self.__baseDir = 0
        self.__limit = memory.size

    @property
    def limit(self):
        return self.__limit

    @limit.setter
    def limit(self, limit):
        self.__limit = limit

    @property
    def baseDir(self):
        return self.__baseDir

    @baseDir.setter
    def baseDir(self, baseDir):
        self.__baseDir = baseDir

    def fetch(self,  logicalAddress):
        if (logicalAddress >= self.__limit):
            raise Exception("Invalid Address,  {logicalAddress} is higher than process limit: {limit}".format(limit = self.__limit, logicalAddress = logicalAddress))

        physicalAddress = logicalAddress + self.__baseDir
        return self.__memory.read(physicalAddress)

    def place(self,  logicalAddress, value):
        if (logicalAddress >= self.__limit):
            raise Exception("Invalid Address,  {logicalAddress} is higher than process limit: {limit}".format(limit = self.__limit, logicalAddress = logicalAddress))

        physicalAddress = logicalAddress + self.__baseDir
        return self.__memory.write(physicalAddress, value)
