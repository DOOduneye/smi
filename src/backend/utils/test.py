queries = [["CREATE_ACCOUNT","1","account1"], ["CREATE_ACCOUNT","2","account2"], 
    ["CREATE_ACCOUNT","3","account3"], 
    ["DEPOSIT","4","account1","1000"], 
    ["DEPOSIT","5","account2","1000"], 
    ["DEPOSIT","6","account3","1000"], 
    ["TRANSFER","7","account2","account3","100"], 
    ["TRANSFER","8","account2","account3","100"], 
    ["TRANSFER","9","account3","account1","100"], 
    ["TOP_SPENDERS","10","3"]]

def solution():
    bank = BankAccount()
    output = []
    for query in queries:
        if query[0] == "CREATE_ACCOUNT":
            output.append(bank.create_account(query[1], query[2]))
        elif query[0] == "DEPOSIT":
            output.append(bank.deposit(query[1], query[2], int(query[3])))
        elif query[0] == "TRANSFER":
            output.append(bank.transfer(query[1], query[2], query[3], int(query[4])))
        elif query[0] == "TOP_SPENDERS":
            output.append(bank.top_spenders(query[1], int(query[2])))
    return output


class BankAccount:
    def __init__(self):
        self.accounts = []
        
    def create_account(self, timestamp: str, account_id: str) -> str:
        for account in self.accounts:
            if account.get_account_id() == account_id:
                return "false"
        
        self.accounts.append(Account(timestamp, account_id))
        return 'true'
        
    def deposit(self, timestamp: str, account_id: str, amount: int) -> str:
        for account in self.accounts:
            if account.get_account_id() == account_id:
                account.increment_account_balance(amount)
                return str(account.get_account_balance())
        
        return ''
        
    def transfer(self, timestamp: str, from_id: str, to_id: str, amount: int) -> str:
        if from_id == to_id:
            return ''
        
        from_account = None
        to_account = None
        
        for account in self.accounts:
            if account.get_account_id() == from_id:
                if account.get_account_balance() < amount:
                    return ''
                from_account = account
            if account.get_account_id() == to_id:
                to_account = account
    
        if from_account == None:
            return ''
        if to_account == None:
            return ''
        
        from_account.decrement_account_balance(amount)
        to_account.increment_account_balance(amount)
        return str(from_account.get_account_balance())
    
    def top_spenders(self, timestamp: str, n: int) -> str:
        output = []
        accounts = sorted(self.accounts, key=lambda x: x.get_account_id())
        accounts = sorted(accounts, key=lambda x: x.get_outgoing(), reverse=True)
        for i in range(n):
            if i >= len(accounts):
                break
            output.append(accounts[i].get_account_id() + '(' + str(accounts[i].get_outgoing()) + ')')
            
        return ', '.join(output)
    
    def schedule_payment(self, timestamp: str, accound_id: str, amount: int, delay: int) -> str:
        payment_time = timestamp + delay
        for account in self.accounts:
            if account.get_account_id() == accound_id:
                account.add_pending_payment(str(payment_time), amount)
                return f'payment{payment_time}'
         
        return ''
        
    # def cancel_payment(self, timestamp: str, accound_id: str, payment_id: str):
        
class Account:
    def __init__(self, timestamp: str, account_id: str):
        self.account_balance = 0
        self.timestamp = timestamp
        self.account_id = account_id
        self.outgoing = 0
        self.pending = []
        
    def add_pending_payment(self, payment_id: str, amount: int) -> None:
        self.pending.append((payment_id, amount))

    def __handle_pending_payments(self, timestamp: int) -> bool:
        #CHEDULE_PAYMENT <timestamp> <accountId> <amount> <delay> — should schedule a payment which will be performed at timestamp + delay. Returns a string with a unique identifier for the scheduled payment in the following format: "payment[ordinal number of the scheduled payment across all accounts]" - e.g., "payment1", "payment2", etc. If accountId doesn't exist, returns an empty string. If the specified account has insufficent funds when the payment is performed, the payment is skipped. Additional conditions:

#Successfully payments should be included when ranking accounts using the TOP_SPENDERS operation.
#Scheduled payments should be processed before any other transactions at the relevant timestamp.
#If an account needs to perform several scheduled payments simultaneously, they should be processed in order of creation - e.g., payment1 should be processed before payment2
        self.pending = sorted(self.pending, key=lambda x: x[0])
        
        for payment in self.pending():
            if payment[0] <= timestamp:
                self.pending.remove(payment)
                if self.account_balance >= payment[1]:
                    self.account_balance -= payment[1]
                    self.outgoing += payment[1]
                    return True
                self.decrement_account_balance(payment[1], timestamp)
                return True
                
            
    def get_outgoing(self) -> int:
        return self.outgoing
    
    def get_account_balance(self) -> int:
        return self.account_balance
        
    def decrement_account_balance(self, amount: int, timestamp: str) -> None:
        self.timestamp = timestamp
        self.__handle_pending_payments(timestamp)
        self.account_balance -= amount
        self.outgoing += amount
        
        
    def increment_account_balance(self, amount: int, timestamp: str) -> None:
        self.timestamp = timestamp
        self.__handle_pending_payments(timestamp)
        self.account_balance += amount
        
    def get_timestamp(self) -> int:
        return self.timestamp
        
    def get_account_id(self) -> int:
        return self.account_id

solution()