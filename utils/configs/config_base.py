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
            curr = curr.get(arg)
            if curr is None:
                return None

        return curr
