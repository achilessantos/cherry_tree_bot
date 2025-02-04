import logging
import logging.handlers


def setup_custom_logger(name):
    # logger settings
    log_file = "log/logs.log"
    log_file_max_size = 1024 * 1024 * 20  # megabytes
    log_num_backups = 3
    log_format = "%(asctime)s [%(levelname)s] %(filename)s/%(funcName)s:%(lineno)s >> %(message)s"
    log_filemode = "w"  # w: overwrite; a: append

    # setup logger
    logging.basicConfig(
        filename=log_file, format=log_format, filemode=log_filemode, level=logging.DEBUG
    )
    rotate_file = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=log_file_max_size, backupCount=log_num_backups
    )
    logger = logging.getLogger(name)
    logger.addHandler(rotate_file)

    # print log messages to console
    console_handler = logging.StreamHandler()
    log_formatter = logging.Formatter(log_format)
    console_handler.setFormatter(log_formatter)
    logger.addHandler(console_handler)

    return logger
