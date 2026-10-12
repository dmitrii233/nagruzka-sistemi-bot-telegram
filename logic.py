import psutil
import time


def get_cpu_usage():
    """
    Returns the current CPU usage as a percentage.
    """
    return psutil.cpu_percent(interval=1)


def get_cpu_per_core():
    """
    Returns a list of CPU usage percentages for each core.
    """
    return psutil.cpu_percent(interval=1, percpu=True)


def get_cpu_frequency():
    """
    Returns the current CPU frequency in MHz.
    """
    freq = psutil.cpu_freq()
    if freq is None:
        return None
    return freq.current


def get_memory_usage():
    """
    Returns the current memory usage as a percentage.
    """
    return psutil.virtual_memory().percent


def get_free_memory():
    """
    Returns the current free memory as a percentage.
    """
    return psutil.virtual_memory().available / psutil.virtual_memory().total * 100


def get_swap_memory():
    """
    Returns the current swap memory usage (as a psutil swap memory object).
    """
    return psutil.swap_memory()


def get_disk_usage():
    """
    Returns a list of dictionaries containing disk partition usage info.
    Each dictionary contains the device, mount point, file system type,
    total, used, free space and usage percentage.
    """
    disk_info = []
    for part in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(part.mountpoint)
            disk_info.append({
                'device': part.device,
                'mountpoint': part.mountpoint,
                'fstype': part.fstype,
                'total': usage.total,
                'used': usage.used,
                'free': usage.free,
                'percent': usage.percent,
            })
        except (PermissionError, OSError):
            pass
    return disk_info


def get_network_usage():
    """
    Returns the current network usage statistics.
    """
    return psutil.net_io_counters()


def get_network_interfaces():
    """
    Returns a dict of network I/O statistics for each network interface.
    """
    return psutil.net_io_counters(pernic=True)


def get_boot_time():
    """
    Returns the system boot time as a unix timestamp.
    """
    return psutil.boot_time()


def get_uptime():
    """
    Returns the system uptime in seconds.
    """
    return time.time() - psutil.boot_time()


def get_battery():
    """
    Returns the current battery status (or None if no battery present).
    """
    return psutil.sensors_battery()


def get_sensors():
    """
    Returns the current sensor temperatures (or an empty dict if unavailable).
    """
    try:
        return psutil.sensors_temperatures(fahrenheit=False)
    except AttributeError:
        return {}


def get_users():
    """
    Returns a list of dictionaries with info about logged-in users.
    """
    users = []
    for user in psutil.users():
        users.append({
            'name': user.name,
            'terminal': user.terminal,
            'host': user.host,
            'started': user.started,
        })
    return users


def get_process_info():
    """
    Returns a list of dictionaries containing information about all running processes.
    Each dictionary contains the process ID, name, CPU usage, and memory usage.
    """
    process_info = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            process_info.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return process_info


def format_bytes(size):
    """
    Converts a byte count into a human-readable string.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"


def format_uptime(seconds):
    """
    Converts seconds into a human-readable uptime string.
    """
    days, remainder = divmod(int(seconds), 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, secs = divmod(remainder, 60)
    if days > 0:
        return f"{days}d {hours}h {minutes}m {secs}s"
    elif hours > 0:
        return f"{hours}h {minutes}m {secs}s"
    else:
        return f"{minutes}m {secs}s"
