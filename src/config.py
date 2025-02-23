import os
from confz import BaseConfig, FileSource


class SYWallaConfig(BaseConfig):
    name: str
    stage: str

    CONFIG_SOURCES = [
        FileSource(
            folder=f"{os.path.dirname(os.path.realpath(__file__))}/config",
            file_from_env="CONFIG_FILE",
        )
    ]
