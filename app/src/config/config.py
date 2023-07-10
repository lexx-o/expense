from omegaconf import OmegaConf

from .directories import directories

config = OmegaConf.load(directories.config/'config.yaml')

