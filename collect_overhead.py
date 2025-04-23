import time
import psutil


def collect_performance_data(duration, interval, output_file):
    """
    Collects CPU and memory usage data at specified intervals over a given duration
    and records the data to a text file.
    :param duration: Total time to collect data, in seconds.
    :param interval: Time between data collections, in seconds.
    :param output_file: File path to record the data.
    """
    with open(output_file, 'w') as file:
        start_time = time.time()
        file.write("Time\tCPU Usage (%)\tMemory Usage (MB)\n")

        while time.time() - start_time < duration:
            # Collect CPU and memory usage
            cpu_usage = psutil.cpu_percent()
            memory_usage = psutil.virtual_memory().used / (1024 ** 2)  # Convert bytes to MB

            # Write the current usage data to the file
            file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}\t{cpu_usage:.2f}\t{memory_usage:.2f}\n")

            # Sleep until the next interval
            time.sleep(interval)


def calculate_averages(input_file):
    """
    Calculates the average CPU and memory usage from a file.
    :param input_file: File path containing the recorded data.
    :return: A tuple of formatted strings representing average CPU usage and memory usage in MB.
    """
    with open(input_file, 'r') as file:
        lines = file.readlines()[1:]  # Skip the header line
        cpu_total = 0
        memory_total = 0
        count = 0

        for line in lines:
            parts = line.split('\t')
            cpu_total += float(parts[1])
            memory_total += float(parts[2])
            count += 1

    average_cpu = cpu_total / count
    average_memory = memory_total / count

    return (f"{average_cpu:.2f}%", f"{average_memory:.2f} MB")


duration = 180
interval = 5
output_file = "./overhead_data.txt"

# collect data
collect_performance_data(duration, interval, output_file)

# calculate and print averages
average_cpu, average_memory = calculate_averages(output_file)
print("Average CPU Usage:", average_cpu)
print("Average Memory Usage:", average_memory)
