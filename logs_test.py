from loguru import logger
import sys
import json

logger.trace("This is a trace message.")
logger.debug("This is a debug message")
logger.info("This is an info message.")
logger.success("This is a success message.")
logger.warning("This is a warning message.")
logger.error("This is an error message.")
logger.critical("This is a critical message.")

logger.remove(0)
logger.add(sys.stderr, serialize=True)
s = json.dumps(logger.critical("critical"))
print(s)
