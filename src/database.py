class Database:

    def __init__(self, filename):
        self.file =  open('test','w+')   

    def store_message(self,message):
        self.file.write(message)
    
    def close(self):
        self.file.close()
        