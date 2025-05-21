import schedule
import time
from app.collector.collector import connect_and_collect_metrics
from app.core.database import SessionLocal
from app.core.models.device import Device
from prometheus_client import Gauge

# Создание метрик для Prometheus
cpu_usage_gauge = Gauge('cpu_usage_percent', 'CPU Usage Percent', ['host_name'])
memory_usage_gauge = Gauge('memory_usage_percent', 'Memory Usage Percent', ['host_name'])
disk_usage_gauge = Gauge('disk_usage_percent', 'Disk Usage Percent', ['host_name'])

# Добавление метрик для I/O и сети
io_read_bytes_gauge = Gauge('io_read_bytes', 'I/O Read Bytes', ['host_name'])
io_write_bytes_gauge = Gauge('io_write_bytes', 'I/O Write Bytes', ['host_name'])
network_bytes_sent_gauge = Gauge('network_bytes_sent', 'Network Bytes Sent', ['host_name'])
network_bytes_recv_gauge = Gauge('network_bytes_recv', 'Network Bytes Received', ['host_name'])

# Добавление дополнительных метрик для Prometheus
cpu_count_gauge = Gauge('cpu_count', 'CPU Core Count', ['host_name'])
memory_total_gauge = Gauge('memory_total', 'Total Memory', ['host_name'])
memory_used_gauge = Gauge('memory_used', 'Used Memory', ['host_name'])
memory_free_gauge = Gauge('memory_free', 'Free Memory', ['host_name'])
disk_total_gauge = Gauge('disk_total', 'Total Disk Space', ['host_name'])
disk_used_gauge = Gauge('disk_used', 'Used Disk Space', ['host_name'])
disk_free_gauge = Gauge('disk_free', 'Free Disk Space', ['host_name'])
io_read_count_gauge = Gauge('io_read_count', 'I/O Read Count', ['host_name'])
io_write_count_gauge = Gauge('io_write_count', 'I/O Write Count', ['host_name'])
network_packets_sent_gauge = Gauge('network_packets_sent', 'Network Packets Sent', ['host_name'])
network_packets_recv_gauge = Gauge('network_packets_recv', 'Network Packets Received', ['host_name'])
device_up_gauge = Gauge('device_up', 'Device availability (1=up, 0=down)', ['host_name'])

# Новые метрики CPU
cpu_load1_gauge = Gauge('cpu_load1', 'CPU load average for 1 min', ['host_name'])
cpu_user_seconds_gauge = Gauge('cpu_seconds_total_user', 'CPU user seconds total', ['host_name'])
cpu_system_seconds_gauge = Gauge('cpu_seconds_total_system', 'CPU system seconds total', ['host_name'])
cpu_iowait_seconds_gauge = Gauge('cpu_seconds_total_iowait', 'CPU iowait seconds total', ['host_name'])

# Новые метрики Memory
swap_total_gauge = Gauge('memory_SwapTotal_bytes', 'Swap total bytes', ['host_name'])
swap_free_gauge = Gauge('memory_SwapFree_bytes', 'Swap free bytes', ['host_name'])
memory_cached_gauge = Gauge('memory_Cached_bytes', 'Memory cached bytes', ['host_name'])
memory_buffers_gauge = Gauge('memory_Buffers_bytes', 'Memory buffers bytes', ['host_name'])

# Новые метрики Disk
disk_io_time_gauge = Gauge('disk_io_time_seconds_total', 'Disk IO time seconds total', ['host_name'])
disk_read_time_gauge = Gauge('disk_read_time_seconds_total', 'Disk read time seconds total', ['host_name'])
disk_write_time_gauge = Gauge('disk_write_time_seconds_total', 'Disk write time seconds total', ['host_name'])
disk_inodes_free_gauge = Gauge('filesystem_inodes_free', 'Filesystem inodes free', ['host_name'])

# Новые метрики Network
network_err_total_gauge = Gauge('network_err_total', 'Network errors total', ['host_name'])
network_dropped_total_gauge = Gauge('network_dropped_total', 'Network dropped packets total', ['host_name'])
tcp_curr_estab_gauge = Gauge('netstat_Tcp_CurrEstab', 'Active TCP connections', ['host_name'])

# Новая метрика Uptime
uptime_seconds_gauge = Gauge('uptime_seconds', 'Node uptime seconds', ['host_name'])

def collect_metrics_from_hosts():
    """
    Сбор метрик с устройств из базы данных.
    """
    db = SessionLocal()
    try:
        devices = db.query(Device).all()
        from app.core.config import settings
        username = settings.SSH_USERNAME
        key_path = settings.SSH_PRIVATE_KEY_PATH
        script_path = settings.METRICS_SCRIPT_PATH

        for device in devices:
            host_name = device.name
            try:
                metrics = connect_and_collect_metrics(
                    device.ip_address, username, key_path, script_path
                )

                # Метрика доступности устройства
                device_up_gauge.labels(host_name=host_name).set(1)

                # --- Новые метрики CPU ---
                cpu = metrics['cpu']
                cpu_load1_gauge.labels(host_name=host_name).set(cpu.get('cpu_load1', 0))
                cpu_user_seconds_gauge.labels(host_name=host_name).set(cpu.get('cpu_seconds_total_user', 0))
                cpu_system_seconds_gauge.labels(host_name=host_name).set(cpu.get('cpu_seconds_total_system', 0))
                cpu_iowait_seconds_gauge.labels(host_name=host_name).set(cpu.get('cpu_seconds_total_iowait', 0))

                # --- Новые метрики Memory ---
                memory = metrics['memory']
                swap_total_gauge.labels(host_name=host_name).set(memory.get('memory_SwapTotal_bytes', 0))
                swap_free_gauge.labels(host_name=host_name).set(memory.get('memory_SwapFree_bytes', 0))
                memory_cached_gauge.labels(host_name=host_name).set(memory.get('memory_Cached_bytes', 0))
                memory_buffers_gauge.labels(host_name=host_name).set(memory.get('memory_Buffers_bytes', 0))

                # --- Новые метрики Disk ---
                disk = metrics['disk']
                disk_io_time_gauge.labels(host_name=host_name).set(disk.get('disk_io_time_seconds_total', 0))
                disk_read_time_gauge.labels(host_name=host_name).set(disk.get('disk_read_time_seconds_total', 0))
                disk_write_time_gauge.labels(host_name=host_name).set(disk.get('disk_write_time_seconds_total', 0))
                disk_inodes_free_gauge.labels(host_name=host_name).set(disk.get('filesystem_inodes_free', 0))

                # --- Новые метрики Network ---
                network = metrics['network']
                network_err_total_gauge.labels(host_name=host_name).set(network.get('network_err_total', 0))
                network_dropped_total_gauge.labels(host_name=host_name).set(network.get('network_dropped_total', 0))
                tcp_curr_estab_gauge.labels(host_name=host_name).set(network.get('netstat_Tcp_CurrEstab', 0))

                # --- Новая метрика Uptime ---
                uptime = metrics['uptime']
                uptime_seconds_gauge.labels(host_name=host_name).set(uptime.get('uptime_seconds', 0))

                # --- Старые метрики ---
                cpu_usage_gauge.labels(host_name=host_name).set(cpu.get('usage_percent', 0))
                memory_usage_gauge.labels(host_name=host_name).set(memory.get('percent', 0))
                disk_usage_gauge.labels(host_name=host_name).set(disk.get('percent', 0))
                io_read_bytes_gauge.labels(host_name=host_name).set(disk.get('read_bytes', 0))
                io_write_bytes_gauge.labels(host_name=host_name).set(disk.get('write_bytes', 0))
                network_bytes_sent_gauge.labels(host_name=host_name).set(network.get('bytes_sent', 0))
                network_bytes_recv_gauge.labels(host_name=host_name).set(network.get('bytes_recv', 0))
                cpu_count_gauge.labels(host_name=host_name).set(cpu.get('count', 0))
                memory_total_gauge.labels(host_name=host_name).set(memory.get('total', 0))
                memory_used_gauge.labels(host_name=host_name).set(memory.get('used', 0))
                memory_free_gauge.labels(host_name=host_name).set(memory.get('free', 0))
                disk_total_gauge.labels(host_name=host_name).set(disk.get('total', 0))
                disk_used_gauge.labels(host_name=host_name).set(disk.get('used', 0))
                disk_free_gauge.labels(host_name=host_name).set(disk.get('free', 0))
                io_read_count_gauge.labels(host_name=host_name).set(disk.get('read_count', 0))
                io_write_count_gauge.labels(host_name=host_name).set(disk.get('write_count', 0))
                network_packets_sent_gauge.labels(host_name=host_name).set(network.get('packets_sent', 0))
                network_packets_recv_gauge.labels(host_name=host_name).set(network.get('packets_recv', 0))

                print(f"Метрики с {host_name} ({device.ip_address}): {metrics}")
            except Exception as e:
                # Метрика доступности устройства
                device_up_gauge.labels(host_name=host_name).set(0)
                print(f"Ошибка при сборе метрик с {device.name} ({device.ip_address}): {e}")
    finally:
        db.close()

# Планирование задачи
schedule.every(30).seconds.do(collect_metrics_from_hosts)

if __name__ == "__main__":
    print("Запуск планировщика задач для сбора метрик...")
    while True:
        schedule.run_pending()
        time.sleep(1)
