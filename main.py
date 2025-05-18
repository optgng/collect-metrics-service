from app import create_app
import uvicorn
import threading
from app.collector import scheduler
from app.core.database import apply_migrations

app = create_app()

# Запуск планировщика задач в отдельном потоке (schedule.run_pending в цикле)
def run_scheduler():
    while True:
        scheduler.schedule.run_pending()
        import time; time.sleep(1)

scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()

# Применение миграций перед запуском приложения
apply_migrations()

if __name__ == "__main__":
    import os
    reload_flag = os.environ.get("FASTAPI_RELOAD", "0") == "1"
    # Исправлено: передаём app, а не строку "main:app"
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=reload_flag)
