import os
from confz import BaseConfig, FileSource


class SYWallaConfig(BaseConfig):
    """Configuration for the stack."""

    student_name: str = "Sergio Yunta Martin"
    name: str
    stage: str
    ad_creation_days_to_expire: str
    web_domain: str

    CONFIG_SOURCES = [
        FileSource(
            folder=f"{os.path.dirname(os.path.realpath(__file__))}/config",
            file_from_env="CONFIG_FILE",
        )
    ]
