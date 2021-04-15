from typing import Optional

from pydantic import BaseModel


class del_file(BaseModel):
    name: str
