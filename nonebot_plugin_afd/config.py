from typing import Optional, Dict

from pydantic import BaseModel, Extra


class Config(BaseModel, extra=Extra.ignore):
    afd_token_list: Optional[Dict[str, Dict[str, str]]] = None
