from abc import ABC, abstractmethod



class DataProcessor(ABC):
    
    def read_data(self):
        print("Reading Data")
        
    @abstractmethod
    def process_data(self):
        pass
    
    def before_process(self):
        pass
    
    def save_result(self):
        print("Saving Data")
    
    def process(self):
        
        self.read_data()
        self.before_process()
        self.process_data()
        self.save_result()
        
        
        
class CSVProcessor(DataProcessor):
    
    def process_data(self):
        print("Processing CSV")
        
        
class JSONProcessor(DataProcessor):
    
    def process_data(self):
        print("Processing JSON")
        
    def before_process(self):
        print("Validating Json depth")
        
        
        
csv_processor=CSVProcessor()
json_processor=JSONProcessor()

csv_processor.process()
json_processor.process()