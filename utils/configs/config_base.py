from typing import Optional, Any


class ConfigBase:
    def __init__(self, config_dict: dict):
        self._config = config_dict

    @property
    def config(self) -> dict:
        return self._config

    def _get(self, *args) -> Optional[Any]:
        curr = self.config
        for arg in args:
            if child := curr.get(arg):
                curr = child
            else:
                return None

        return curr
