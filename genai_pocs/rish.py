from rich.console import Console
from rich.live import Live
from rich.table import Table
import time
import psutil

def system_stats():
        table = Table(title="System Stats")
        table.add_column("Metric")
        table.add_column("Value")
        table.add_column("Description")

        cpu_percent = psutil.cpu_percent(interval=1)
        mem_info = psutil.virtual_memory()
        net_io = psutil.net_io_counters()

        table.add_row("CPU Usage", f"{cpu_percent}%", "Current CPU utilization")
        table.add_row("Memory Used", f"{mem_info.percent}%", "Memory usage percentage")
        table.add_row("Network Sent", f"{net_io.bytes_sent / (1024**2):.2f} MB", "Data sent over network")
        table.add_row("Network Received", f"{net_io.bytes_recv / (1024**2):.2f} MB", "Data received over network")

        return table

console = Console()
with Live(system_stats(), refresh_per_second=1) as live:
        while True:
            live.update(system_stats())
            time.sleep(1)
