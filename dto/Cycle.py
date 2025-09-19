from __future__ import annotations

from typing import Optional, Any, Dict, List
from .SearchObjectList import SearchObjectList
from .TestCase import TestCase
from pydantic import BaseModel, ConfigDict


class Cycle(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    searchObjectList: Optional[List[TestCase]] = None
    summaryList: Optional[str] = None
    totalCount: Optional[int] = None
    currentOffset: Optional[int] = None
    maxAllowed: Optional[int] = None
    maxAllowedforSelect: Optional[int] = None
    sortBy: Optional[str] = None
    sortOrder: Optional[str] = None
    executionStatus: Optional[Dict] = None
    stepExecutionStatus: Optional[Dict] = None

    def __str__(self):
        return self.model_dump_json(indent=4)