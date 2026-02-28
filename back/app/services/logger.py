import logging
from logging.handlers import RotatingFileHandler

class LoggerService:
    """Loggers da aplicação"""
    
    def __init__(self, name: str = "app_logger"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            formatter = logging.Formatter(
                fmt="%(asctime)s | %(levelname)s | %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            # Log no arquivo com rotação (evita arquivo gigante)
            file_handler = RotatingFileHandler(
                "app.log",
                maxBytes=5_000_000,  # 5MB
                backupCount=3
            )
            file_handler.setFormatter(formatter)

            # Log no console
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def log(self, route: str, method: str, message: str, level: str = "info"):
        log_message = f"Route: {route} | Method: {method} | Message: {message}"

        level = level.lower()

        if level == "debug":
            self.logger.debug(log_message)
        elif level == "warning":
            self.logger.warning(log_message)
        elif level == "error":
            self.logger.error(log_message)
        elif level == "critical":
            self.logger.critical(log_message)
        else:
            self.logger.info(log_message)