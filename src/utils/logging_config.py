import logging

logging.basicConfig(
    filename="collection_process.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

console_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(console_formatter)

logger.addHandler(console_handler)
