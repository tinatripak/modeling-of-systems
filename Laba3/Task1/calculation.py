from Task1.process import Process
    
def get_meanload(e: Process, tcurr):
    return e.meanload / tcurr

def get_meanqueue_len(e: Process, tcurr):
    return e.meanqueue / tcurr

def get_failure_probability(e: Process):
    return e.failure / (e.quantity + e.failure) if (e.quantity + e.failure) != 0 else 0

def get_result(sum, count):
    return sum/count