import telebot
from logic import (get_cpu_usage, get_cpu_per_core, get_cpu_frequency,
                   get_memory_usage, get_free_memory, get_swap_memory,
                   get_network_usage, get_network_interfaces, get_disk_usage,
                   get_boot_time, get_uptime, get_battery, get_sensors,
                   get_users, get_process_info, format_bytes, format_uptime)
from config import token

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['cpu'])
def send_cpu_usage(message):
    cpu_usage = get_cpu_usage()
    bot.reply_to(message, f"Current CPU usage: {cpu_usage}%")


@bot.message_handler(commands=['cores'])
def send_cpu_per_core(message):
    cores = get_cpu_per_core()
    response = "CPU usage per core:\n"
    for i, usage in enumerate(cores):
        response += f"Core {i}: {usage}%\n"
    bot.reply_to(message, response)


@bot.message_handler(commands=['cpu_freq'])
def send_cpu_frequency(message):
    freq = get_cpu_frequency()
    if freq is None:
        bot.reply_to(message, "CPU frequency is not available.")
    else:
        bot.reply_to(message, f"Current CPU frequency: {freq:.2f} MHz")


@bot.message_handler(commands=['memory'])
def send_memory_usage(message):
    memory_usage = get_memory_usage()
    bot.reply_to(message, f"Current memory usage: {memory_usage}%")


@bot.message_handler(commands=['free_memory'])
def send_free_memory(message):
    free_memory = get_free_memory()
    bot.reply_to(message, f"Current free memory: {free_memory:.2f}%")


@bot.message_handler(commands=['swap'])
def send_swap_memory(message):
    swap = get_swap_memory()
    bot.reply_to(message, f"Swap usage:\n"
                          f"Total: {format_bytes(swap.total)}\n"
                          f"Used: {format_bytes(swap.used)}\n"
                          f"Free: {format_bytes(swap.free)}\n"
                          f"Usage: {swap.percent}%")


@bot.message_handler(commands=['uptime'])
def send_uptime(message):
    uptime = get_uptime()
    bot.reply_to(message, f"System uptime: {format_uptime(uptime)}")


@bot.message_handler(commands=['disk'])
def send_disk_usage(message):
    disks = get_disk_usage()
    response = "Disk usage:\n"
    for disk in disks:
        response += (f"{disk['device']} ({disk['mountpoint']}, {disk['fstype']}):\n"
                     f"  Total: {format_bytes(disk['total'])}\n"
                     f"  Used: {format_bytes(disk['used'])} ({disk['percent']}%)\n"
                     f"  Free: {format_bytes(disk['free'])}\n")
    bot.reply_to(message, response)


@bot.message_handler(commands=['system'])
def send_system_usage(message):
    cpu_usage = get_cpu_usage()
    memory_usage = get_memory_usage()
    free_memory = get_free_memory()
    network_usage = get_network_usage()
    bot.reply_to(message, f"Current CPU usage: {cpu_usage}%\n"
                          f"Current Memory usage: {memory_usage}%\n"
                          f"Free Memory: {free_memory:.2f}%\n"
                          f"Network usage:\n"
                          f"Bytes sent: {format_bytes(network_usage.bytes_sent)}\n"
                          f"Bytes received: {format_bytes(network_usage.bytes_recv)}")


@bot.message_handler(commands=['network'])
def send_network_usage(message):
    network_usage = get_network_usage()
    bot.reply_to(message, f"Network usage:\n"
                          f"Bytes sent: {format_bytes(network_usage.bytes_sent)}\n"
                          f"Bytes received: {format_bytes(network_usage.bytes_recv)}")


@bot.message_handler(commands=['interfaces'])
def send_network_interfaces(message):
    interfaces = get_network_interfaces()
    response = "Network interfaces:\n"
    for name, counters in interfaces.items():
        response += (f"{name}:\n"
                     f"  Sent: {format_bytes(counters.bytes_sent)}\n"
                     f"  Received: {format_bytes(counters.bytes_recv)}\n")
    bot.reply_to(message, response)


@bot.message_handler(commands=['battery'])
def send_battery(message):
    battery = get_battery()
    if battery is None:
        bot.reply_to(message, "No battery found (probably a desktop PC).")
    else:
        bot.reply_to(message, f"Battery status:\n"
                              f"Charge: {battery.percent}%\n"
                              f"Plugged in: {'Yes' if battery.power_plugged else 'No'}")


@bot.message_handler(commands=['sensors'])
def send_sensors(message):
    temps = get_sensors()
    if not temps:
        bot.reply_to(message, "No temperature sensors available.")
        return
    response = "Temperature sensors:\n"
    for name, entries in temps.items():
        for entry in entries:
            response += f"{name} ({entry.label or 'sensor'}): {entry.current:.1f}°C\n"
            if len(response) > 2048:
                bot.reply_to(message, response)
                response = "Temperature sensors:\n"
    bot.reply_to(message, response)


@bot.message_handler(commands=['users'])
def send_users(message):
    users = get_users()
    if not users:
        bot.reply_to(message, "No logged-in users found.")
        return
    response = "Logged-in users:\n"
    for user in users:
        response += (f"Name: {user['name']}\n"
                     f"Terminal: {user['terminal']}\n"
                     f"Host: {user['host']}\n\n")
    bot.reply_to(message, response)


@bot.message_handler(commands=['processes'])
def send_process_info(message):
    process_info = get_process_info()
    response = "Running processes:\n"
    for proc in process_info:
        response += f"PID: {proc['pid']}, Name: {proc['name']}, CPU: {proc['cpu_percent']}%, Memory: {proc['memory_percent']:.2f}%\n"
        if len(response) > 2048:
            bot.reply_to(message, response)
            response = "Running processes:\n"
    bot.reply_to(message, response)


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Available commands:\n"
                          "/cpu - CPU usage\n"
                          "/cores - CPU usage per core\n"
                          "/cpu_freq - CPU frequency\n"
                          "/memory - Memory usage\n"
                          "/free_memory - Free memory\n"
                          "/swap - Swap memory\n"
                          "/disk - Disk usage\n"
                          "/uptime - System uptime\n"
                          "/network - Network usage (total)\n"
                          "/interfaces - Network usage per interface\n"
                          "/battery - Battery status\n"
                          "/sensors - Temperature sensors\n"
                          "/users - Logged-in users\n"
                          "/processes - Running processes\n"
                          "/system - Overall system stats\n"
                          "/help - Show this help")


if __name__ == "__main__":
    bot.infinity_polling()
