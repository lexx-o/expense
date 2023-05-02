from pathlib import Path


class _Directories:
    def __init__(self):
        self.root = Path(__file__).parents[2].resolve()
        self.config = self.root/'config'
        self.package = self.root/'src'


directories = _Directories()
