from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="SERVICE_",
    settings_files=["settings.toml"],
    environments=True,
    env_switcher="SERVICE_ENV",
    default_env="default"
)

APP_NAME = settings.APP_NAME
DEBUG = settings.DEBUG
DB_URL = getattr(settings, "DB_URL", None)
DB_HOST = getattr(settings, "DB_HOST", None)
DB_PORT = getattr(settings, "DB_PORT", None)
DB_NAME = getattr(settings, "DB_NAME", None)
DB_USER = getattr(settings, "DB_USER", None)
DB_PASSWORD = getattr(settings, "DB_PASSWORD", None)
FEATURE_FLAG_NEW_LOGIC = getattr(settings, "FEATURE_FLAG_NEW_LOGIC", False)
SSH_PRIVATE_KEY_PATH = getattr(settings, "SSH_PRIVATE_KEY_PATH", None)

SSH_USERNAME = getattr(settings, "SSH_USERNAME", None)
METRICS_SCRIPT_PATH = getattr(settings, "METRICS_SCRIPT_PATH", None)
