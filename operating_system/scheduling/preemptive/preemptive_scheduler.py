from operating_system.scheduling.abstract_scheduler import AbtractSchedulerAlgorithm

class PreemptiveSchedulerAlgorithm(AbtractSchedulerAlgorithm):

    @property
    def is_preemptive(self):
        """ Answers if this algorithm is preemptive or not. """
        return True