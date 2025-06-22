import asyncio
import logging
import os
import sys

from app import main
from config.config import Config, load_config

config: Config = load_config()

logging.basicConfig(
    level=logging.getLevelName(level=config.log.level),
    format=config.log.format
)

if __name__ == '__main__':
    asyncio.run(main(config))