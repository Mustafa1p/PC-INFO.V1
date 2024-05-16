import psutil
import platform
import tkinter as tk
from tkinter import ttk
import subprocess
# Don't change or still this code | follow me on instagram @tofa
class PCInfoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PC Information | By Mustafa ip")
        
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0)

        # Initialize disks variable
        self.disks = psutil.disk_partitions()
        
        self.create_widgets()
    
    def create_widgets(self):
        # System Info
        ttk.Label(self.main_frame, text="System Information", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        ttk.Label(self.main_frame, text=f"Operating System: {platform.system()} {platform.release()}").grid(row=1, column=0, columnspan=2, sticky="w")
        ttk.Label(self.main_frame, text=f"Processor: {platform.processor()}").grid(row=2, column=0, columnspan=2, sticky="w")
        ttk.Label(self.main_frame, text=f"Motherboard: {self.get_motherboard_info()}").grid(row=3, column=0, columnspan=2, sticky="w")
        ttk.Label(self.main_frame, text=f"Screen Resolution: {self.get_screen_resolution()}").grid(row=4, column=0, columnspan=2, sticky="w")
        
        # Memory Info
        memory = psutil.virtual_memory()
        ttk.Label(self.main_frame, text="Memory Information", font=("Arial", 14, "bold")).grid(row=5, column=0, columnspan=2, pady=10)
        ttk.Label(self.main_frame, text=f"Total Memory: {self.format_bytes(memory.total)}").grid(row=6, column=0, columnspan=2, sticky="w")
        ttk.Label(self.main_frame, text=f"Available Memory: {self.format_bytes(memory.available)}").grid(row=7, column=0, columnspan=2, sticky="w")
        
        # Disk Info
        ttk.Label(self.main_frame, text="Disk Information", font=("Arial", 14, "bold")).grid(row=8, column=0, columnspan=2, pady=10)
        for i, disk in enumerate(self.disks):
            ttk.Label(self.main_frame, text=f"Disk {i+1} Name: {disk.device}").grid(row=9+i*2, column=0, sticky="w")
            disk_usage = psutil.disk_usage(disk.mountpoint)
            ttk.Label(self.main_frame, text=f"    Total Space: {self.format_bytes(disk_usage.total)}").grid(row=10+i*2, column=0, sticky="w")
            ttk.Label(self.main_frame, text=f"    Free Space: {self.format_bytes(disk_usage.free)}").grid(row=11+i*2, column=0, sticky="w")
        
        # GPU Info
        ttk.Label(self.main_frame, text="GPU Information", font=("Arial", 14, "bold")).grid(row=12+len(self.disks)*2, column=0, columnspan=2, pady=10)
        ttk.Label(self.main_frame, text=f"GPU: {self.get_gpu_info()}").grid(row=13+len(self.disks)*2, column=0, columnspan=2, sticky="w")
        
        # Internet Info
        ttk.Label(self.main_frame, text="Internet Information", font=("Arial", 14, "bold")).grid(row=14+len(self.disks)*2, column=0, columnspan=2, pady=10)
        ttk.Label(self.main_frame, text=f"Internet Status: {'Connected' if self.check_internet() else 'Disconnected'}").grid(row=15+len(self.disks)*2, column=0, columnspan=2, sticky="w")

        
    def check_internet(self):
        try:
            import urllib.request
            urllib.request.urlopen('http://google.com', timeout=1)
            return True
        except urllib.request.URLError:
            return False
    
    def format_bytes(self, bytes):
        # Format bytes to human readable format
        if bytes < 1024:
            return f"{bytes} B"
        elif bytes < 1024**2:
            return f"{bytes/1024:.2f} KB"
        elif bytes < 1024**3:
            return f"{bytes/1024**2:.2f} MB"
        else:
            return f"{bytes/1024**3:.2f} GB"
    
    def get_motherboard_info(self):
        # Get motherboard information using subprocess
        try:
            result = subprocess.check_output("wmic baseboard get product,Manufacturer,version,serialnumber", shell=True).decode().strip()
            return result.split('\n')[1].strip()
        except:
            return "Unknown"
    
    def get_gpu_info(self):
        # Get GPU information using subprocess
        try:
            result = subprocess.check_output("wmic path win32_videocontroller get name", shell=True).decode().strip()
            return result.split('\n')[1].strip()
        except:
            return "Unknown"
    
    def get_screen_resolution(self):
        # Get screen resolution using tkinter
        return f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}"

if __name__ == "__main__":
    root = tk.Tk()
    app = PCInfoApp(root)
    root.mainloop()
