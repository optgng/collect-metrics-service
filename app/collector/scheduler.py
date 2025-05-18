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

                # Обновление метрик для Prometheus
                cpu_usage_gauge.labels(host_name=host_name).set(metrics['cpu']['usage_percent'])
                memory_usage_gauge.labels(host_name=host_name).set(metrics['memory']['percent'])
                disk_usage_gauge.labels(host_name=host_name).set(metrics['disk']['percent'])

                # Обновление метрик для I/O и сети
                io_read_bytes_gauge.labels(host_name=host_name).set(metrics['io']['read_bytes'])
                io_write_bytes_gauge.labels(host_name=host_name).set(metrics['io']['write_bytes'])
                network_bytes_sent_gauge.labels(host_name=host_name).set(metrics['network']['bytes_sent'])
                network_bytes_recv_gauge.labels(host_name=host_name).set(metrics['network']['bytes_recv'])

                # Обновление дополнительных метрик для Prometheus
                cpu_count_gauge.labels(host_name=host_name).set(metrics['cpu']['count'])
                memory_total_gauge.labels(host_name=host_name).set(metrics['memory']['total'])
                memory_used_gauge.labels(host_name=host_name).set(metrics['memory']['used'])
                memory_free_gauge.labels(host_name=host_name).set(metrics['memory']['free'])
                disk_total_gauge.labels(host_name=host_name).set(metrics['disk']['total'])
                disk_used_gauge.labels(host_name=host_name).set(metrics['disk']['used'])
                disk_free_gauge.labels(host_name=host_name).set(metrics['disk']['free'])
                io_read_count_gauge.labels(host_name=host_name).set(metrics['io']['read_count'])
                io_write_count_gauge.labels(host_name=host_name).set(metrics['io']['write_count'])
                network_packets_sent_gauge.labels(host_name=host_name).set(metrics['network']['packets_sent'])
                network_packets_recv_gauge.labels(host_name=host_name).set(metrics['network']['packets_recv'])

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
