import psutil
import json

def collect_metrics():
    """
    Сбор метрик по CPU, RAM, дисковому пространству, операциям ввода-вывода и сетевым метрикам.
    """
    metrics = {
        "cpu": {
            "usage_percent": psutil.cpu_percent(interval=1),
            "count": psutil.cpu_count()
        },
        "memory": {
            "total": psutil.virtual_memory().total,
            "used": psutil.virtual_memory().used,
            "free": psutil.virtual_memory().free,
            "percent": psutil.virtual_memory().percent
        },
        "disk": {
            "total": psutil.disk_usage('/').total,
            "used": psutil.disk_usage('/').used,
            "free": psutil.disk_usage('/').free,
            "percent": psutil.disk_usage('/').percent
        },
        "io": {
            "read_count": psutil.disk_io_counters().read_count,
            "write_count": psutil.disk_io_counters().write_count,
            "read_bytes": psutil.disk_io_counters().read_bytes,
            "write_bytes": psutil.disk_io_counters().write_bytes
        },
        "network": {
            "bytes_sent": psutil.net_io_counters().bytes_sent,
            "bytes_recv": psutil.net_io_counters().bytes_recv,
            "packets_sent": psutil.net_io_counters().packets_sent,
            "packets_recv": psutil.net_io_counters().packets_recv
        }
    }
    return metrics

if __name__ == "__main__":
    metrics = collect_metrics()
    print(json.dumps(metrics, indent=4))
