import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOGS_DIR = Path("logs")
LOGS_DIR.mkdir(parents=True, exist_ok=True)


def get_logger(name: str = "tests", level: int = logging.INFO) -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console = logging.StreamHandler()
    console.setFormatter(formatter)

    file_handler = RotatingFileHandler(LOGS_DIR / "tests.log", maxBytes=5_000_000, backupCount=3)
    file_handler.setFormatter(formatter)

    logger.addHandler(console)
    logger.addHandler(file_handler)
    logger.propagate = False

    return logger