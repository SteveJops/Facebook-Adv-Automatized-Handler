from dataclasses import dataclass, field
from typing import Dict, Optional, Any


@dataclass(frozen=True)
class FbData:
    """Cls for getting a list of ids

    Returns:
        list: app`s ids
    """
    app_id: list = field(default_factory=list)

    def __iter__(self):
        """to get the method itterable

        Returns:
            itterable obj
        """        
        return self.app_id.__iter__()

    def to_response(self)-> Dict[str, Optional[int]]:
        """get the whole data

        Returns:
            Dict[str, Optional[int]]: dict with whole data in the list as value
        """
        return self.__dict__
    

@dataclass(frozen=True)
class AddedApps:
    """Cls for getting advertisement app`s ids
    """
    app_id_with_approvings_and_not: dict = field(default_factory=dict)

    def to_response(self) -> Dict[Any, Any]:
        """method to get the dict with needy data

        Returns:
            Dict[int, Any]: data as value of the whole dict
        """
        return self.app_id_with_approvings_and_not
