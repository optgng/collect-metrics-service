import psutil
import json
import time
import os

def collect_metrics():
    """
    Сбор метрик по CPU, RAM, дисковому пространству, операциям ввода-вывода, сетевым метрикам и аптайму.
    """
    # CPU
    cpu_times = psutil.cpu_times()
    cpu_metrics = {
        "cpu_load1": os.getloadavg()[0] if hasattr(os, "getloadavg") else 0.0,
        "cpu_seconds_total_user": cpu_times.user,
        "cpu_seconds_total_system": cpu_times.system,
        "cpu_seconds_total_iowait": getattr(cpu_times, "iowait", 0.0),
        "usage_percent": psutil.cpu_percent(interval=1),
        "count": psutil.cpu_count()
    }

    # Memory
    vm = psutil.virtual_memory()
    sm = psutil.swap_memory()
    memory_metrics = {
        "memory_SwapTotal_bytes": sm.total,
        "memory_SwapFree_bytes": sm.free,
        "memory_Cached_bytes": getattr(vm, "cached", 0),
        "memory_Buffers_bytes": getattr(vm, "buffers", 0),
        "total": vm.total,
        "used": vm.used,
        "free": vm.free,
        "percent": vm.percent
    }

    # Disk
    disk = psutil.disk_usage('/')
    disk_io = psutil.disk_io_counters()
    disk_metrics = {
        "disk_io_time_seconds_total": getattr(disk_io, "busy_time", 0) / 1000 if hasattr(disk_io, "busy_time") else 0,
        "disk_read_time_seconds_total": getattr(disk_io, "read_time", 0) / 1000,
        "disk_write_time_seconds_total": getattr(disk_io, "write_time", 0) / 1000,
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percent": disk.percent,
        "read_count": disk_io.read_count,
        "write_count": disk_io.write_count,
        "read_bytes": disk_io.read_bytes,
        "write_bytes": disk_io.write_bytes
    }
    # Inodes free (Linux only)
    try:
        st = os.statvfs('/')
        disk_metrics["filesystem_inodes_free"] = st.f_favail
    except Exception:
        pass

    # Network
    net_io = psutil.net_io_counters()
    net_metrics = {
        "network_err_total": getattr(net_io, "errin", 0) + getattr(net_io, "errout", 0),
        "network_dropped_total": getattr(net_io, "dropin", 0) + getattr(net_io, "dropout", 0),
        "netstat_Tcp_CurrEstab": 0,  # Заполняется ниже
        "bytes_sent": net_io.bytes_sent,
        "bytes_recv": net_io.bytes_recv,
        "packets_sent": net_io.packets_sent,
        "packets_recv": net_io.packets_recv
    }
    # Активные TCP-соединения
    try:
        net_metrics["netstat_Tcp_CurrEstab"] = len([c for c in psutil.net_connections(kind="tcp") if c.status == "ESTABLISHED"])
    except Exception:
        pass

    # Uptime
    uptime_metrics = {
        "uptime_seconds": int(time.time() - psutil.boot_time())
    }

    metrics = {
        "cpu": cpu_metrics,
        "memory": memory_metrics,
        "disk": disk_metrics,
        "network": net_metrics,
        "uptime": uptime_metrics
    }
    return metrics

if __name__ == "__main__":
    metrics = collect_metrics()
    print(json.dumps(metrics, indent=4))
