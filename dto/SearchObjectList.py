from __future__ import annotations

import json
from pydantic import BaseModel, ConfigDict

from .TestCase import TestCase
from typing import Optional

class SearchObjectList(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    searchObjectList: Optional[list[TestCase]] = None

    def __str__(self):
        return self.model_dump_json(indent=4)