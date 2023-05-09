import yaml
from dataclasses import dataclass

from .directories import directories


@dataclass
class Config:
    token: str
    folders: dict
    schema: str


def _load_base_config_file(path):
    with open(path, 'r') as f:
        out = yaml.safe_load(f)
    return out



def get_config() -> Config:
    config = _load_base_config_file(directories.config / 'config.yaml')
    return Config(**config)


config = get_config()

