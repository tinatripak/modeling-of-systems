from Task2.process import BankProcess

def get_mean_departure_time(e: BankProcess):
    return e.departure_meanTime / e.quantity

def get_mean_bank_time(e: BankProcess):
    return e.bank_meanTime / e.quantity

def get_mean_client(client, tcurr):
    return client / tcurr

def get_result(sum, count): 
    return sum / count