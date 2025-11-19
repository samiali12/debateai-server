from database.session import session

class SummerizationRepository:
    def __init__(self):
        self.db = session()

    
