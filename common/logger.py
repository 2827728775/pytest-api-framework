"""统一日志。"""
import logging

logger = logging.getLogger("api_framework")
logger.setLevel(logging.INFO)

if not logger.handlers:
    _handler = logging.StreamHandler()
    _fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    _handler.setFormatter(_fmt)
    logger.addHandler(_handler)
