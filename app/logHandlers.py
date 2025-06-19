import logging
import os
import sys
import platform
import socket
from zoneinfo import ZoneInfo
from datetime import datetime
from opentelemetry.sdk._logs import LoggingHandler, LoggerProvider
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor, ConsoleLogExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry._logs import set_logger_provider

def logger_setup(args):
    if args.app is None:
        APP_NAME = 'SE_Discord_Bot'
    if args.version is None:
        VERSION ='1.0.0 (DEFAULT)'
    if args.port is None:
        PORT = 9292
    TIMEZONE_REGION = str(datetime.now().astimezone().tzinfo)
    log_location='logs/test_bot.log'
    SERVER_ID = os.getenv('GENERAL_CHANNEL_ID')
    HOSTING = f'http://localhost:{PORT}'
    logger = logging.getLogger(__name__)
    
    logger.info(f"{APP_NAME.istitle()} Log Record Started:\nSetting Up OLTP Log Export Service at: {HOSTING}")
    os.makedirs("logs", exist_ok=True)
    
    file_handler = logging.FileHandler(filename=log_location,encoding='utf-8')
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    full_formatter = logging.Formatter('====================\nDATE TIME:\t%(asctime)s\nLOG LEVEL:\t%(levelname)s\nPROCESS ID:\t%(process)d\nPROCESS:\t%(processName)s\nLOG CAPTURE:[%(name)s]\nFILE:\t%(filename)s\nCONTENTS:\t%(message)s\n=====================')
    
    file_handler.setFormatter(full_formatter)
    stream_handler.setFormatter(full_formatter)
    
    logger.info("Formatters attached to handlers.")
    
    handler_config = [ file_handler, stream_handler ]
    logger.info(f'Handlers Created: Starting dual stream to stdout and {log_location}')
    logging.basicConfig(level=logging.DEBUG, handlers=handler_config)
    
    logger.debug(f"Creating {APP_NAME} Resource")
    
    bot_resource = Resource(attributes={"service.app": APP_NAME,
                                        "service.app.owner": "Software-Engineering-Club",
                                        "service.app.version": VERSION,
                                        "service.app.environment": "Development",
                                        "service.app.features": "Word Swap, Magic 8 Ball, Old Magic 8 Ball",
                                        "service.app.python": sys.version,
                                        "service.app.python.info": sys.version_info,
                                        "service.app.python.exe": sys.executable,
                                        "service.app.python.implementation": platform.python_implementation(),
                                        "service.node": platform.system(),
                                        "service.node.release": platform.release(),
                                        "service.node.process": os.getpid(),
                                        "service.node.hostname": socket.gethostname(),
                                        "service.node.port": HOSTING,
                                        "service.node.machine":platform.machine(),
                                        "service.node.machine.processor": platform.processor(),
                                        "service.node.timezone": TIMEZONE_REGION,
                                        "service.target": "Discord",
                                        "service.target.id":SERVER_ID})

    
    logger.debug("Building and Switching to Open Telemetry Language Protocol")

    resourced_logger = LoggerProvider(resource=bot_resource)
    otlp_exporter = ConsoleLogExporter()
    set_logger_provider(resourced_logger)
    resourced_logger.add_log_record_processor(BatchLogRecordProcessor(otlp_exporter))
    otel_handler = LoggingHandler(level=logging.NOTSET, logger_provider=resourced_logger)
    logger.addHandler(otel_handler)
    logger.removeHandler(stream_handler)
    otel_handler.setFormatter(full_formatter)
    logger.info(f"OTLP Logger Service Configured:Operation Success...")

    handler_config = [otel_handler, file_handler]

    logger.debug(f"Log Handlers Configured")

    logger.info(f"Log Record Set Up Complete")
    return handler_config
