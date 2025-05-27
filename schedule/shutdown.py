

def RUN(scheduler_object):
    if scheduler_object.running:
        scheduler_object.shutdown(wait=False)
        print("Scheduler has been shut down.")