

class Loader:
    
    def __init__(self):
        self.total_written = 0
        
    def __call__(self, file_name, bytes_written, total_bytes):
        self.total_written += bytes_written
        print(f">>> {self.total_written/total_bytes*100:2.2f} %")
