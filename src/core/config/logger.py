LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "logging.Formatter",
            "fmt": "#%(levelname)s [%(asctime)s] %(filename)s:%(lineno)d - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        # Silence h11_impl logs (especially Chrome DevTools noise)
        "h11_impl": {
            "handlers": ["console"],
            "level": "WARNING",  # or "ERROR" to hide completely
            "propagate": False,
        },
        # Default configuration for all other loggers
        "": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}