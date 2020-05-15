import psutil
import platform
import tkinter as tk
from tkinter import ttk
from datetime import datetime

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

# Memory Information
print("="*40, "Memory Information", "="*40)
# get the memory details
svmem = psutil.virtual_memory()
print(f"Total: {get_size(svmem.total)}")
print(f"Available: {get_size(svmem.available)}")
print(f"Used: {get_size(svmem.used)}")
print(f"Percentage: {svmem.percent}%")
print("="*20, "SWAP", "="*20)
# get the swap memory details (if exists)
swap = psutil.swap_memory()
print(f"Total: {get_size(swap.total)}")
print(f"Free: {get_size(swap.free)}")
print(f"Used: {get_size(swap.used)}")
print(f"Percentage: {swap.percent}%")

# Disk Information
print("="*40, "Disk Information", "="*40)
print("Partitions and Usage:")
# get all disk partitions
partitions = psutil.disk_partitions()
for partition in partitions:
    print(f"=== Device: {partition.device} ===")
    print(f"  Mountpoint: {partition.mountpoint}")
    print(f"  File system type: {partition.fstype}")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    print(f"  Total Size: {get_size(partition_usage.total)}")
    print(f"  Used: {get_size(partition_usage.used)}")
    print(f"  Free: {get_size(partition_usage.free)}")
    print(f"  Percentage: {partition_usage.percent}%")
# get IO statistics since boot
disk_io = psutil.disk_io_counters()
print(f"Total read: {get_size(disk_io.read_bytes)}")
print(f"Total write: {get_size(disk_io.write_bytes)}")

# Network information
print("="*40, "Network Information", "="*40)
# get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f"=== Interface: {interface_name} ===")
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f"  IP Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast IP: {address.broadcast}")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print(f"  MAC Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast MAC: {address.broadcast}")
# get IO statistics since boot
net_io = psutil.net_io_counters()
print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")


# intializing the window
window = tk.Tk()
window.title("Info Lite")
# configuring size of the window 
window.geometry('500x400')
#Create Tab Control
TAB_CONTROL = ttk.Notebook(window)
#Tab1
TAB1 = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(TAB1, text='Sys Info')
#Tab2
TAB2 = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(TAB2, text='CPU Info')
TAB_CONTROL.pack(expand=1, fill="both")
#Tab3
TAB3 = ttk.Frame(TAB_CONTROL)
TAB_CONTROL.add(TAB3, text='Mem Info')
#Tab Name Labels
uname = platform.uname()
boot_time_timestamp = psutil.boot_time()
bt = datetime.fromtimestamp(boot_time_timestamp)
ttk.Label(TAB1, text="System Info").grid(column=0, row=0, padx=10, pady=10)
ttk.Label(TAB1, text=f"System: {uname.system}").grid(column=0, row=1, padx=10, pady=1)
ttk.Label(TAB1, text=f"Node Name: {uname.node}").grid(column=0, row=2, padx=10, pady=1)
ttk.Label(TAB1, text=f"Release: {uname.release}").grid(column=0, row=3, padx=10, pady=1)
ttk.Label(TAB1, text=f"Version: {uname.version}").grid(column=0, row=4, padx=10, pady=1)
ttk.Label(TAB1, text=f"Machine: {uname.machine}").grid(column=0, row=5, padx=10, pady=1)
ttk.Label(TAB1, text=f"Processor: {uname.processor}").grid(column=0, row=6, padx=10, pady=1)
ttk.Label(TAB1, text=f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}").grid(column=0, row=7, padx=10, pady=1)

cpufreq = psutil.cpu_freq()
ttk.Label(TAB2, text="System Info").grid(column=0, row=0, padx=10, pady=10)
ttk.Label(TAB2, text=f"Physical cores: {psutil.cpu_count(logical=False)}").grid(column=0, row=1, padx=10, pady=10)
ttk.Label(TAB2, text=f"Total cores:{psutil.cpu_count(logical=True)}", ).grid(column=0, row=2, padx=10, pady=10)
ttk.Label(TAB2, text=f"Max Frequency: {cpufreq.max:.2f}Mhz").grid(column=0, row=3, padx=10, pady=10)
ttk.Label(TAB2, text=f"Min Frequency: {cpufreq.min:.2f}Mhz").grid(column=0, row=4, padx=10, pady=10)
ttk.Label(TAB2, text=f"Current Frequency: {cpufreq.current:.2f}Mhz").grid(column=0, row=5, padx=10, pady=10)
ttk.Label(TAB2, text="CPU Usage Per Core:").grid(column=0, row=6, padx=10, pady=10)
rowad = 7
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    ttk.Label(TAB2, text=f"Core {i}: {percentage}%").grid(column=0, row=rowad, padx=10, pady=10)
    rowad = rowad + 1
ttk.Label(TAB2, text=f"Total CPU Usage: {psutil.cpu_percent()}%").grid(column=0, row=rowad + 1, padx=10, pady=10)

ttk.Label(TAB3, text="This is Tab 3").grid(column=0, row= 2, padx=10, pady=10)

#Calling Main()
window.mainloop()