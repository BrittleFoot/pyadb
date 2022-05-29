

class Loader:
    
    def __init__(self):
        self.total_written = 0
        
    def __call__(self, file_name, bytes_written, total_bytes):
        self.total_written += bytes_written
        percent = self.total_written / total_bytes
        end = '\n' if abs(1 - percent) < 1e-6 else '\r'
        print(f">>> {percent*100:2.2f} %", end=end)
