from dataclasses import dataclass
from typing import Optional
from pydantic import BaseModel, ConfigDict

class TestCaseStatus(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    name: Optional[str] = None
    testCaseId: Optional[int] = None
    description: Optional[str] = None
    color: Optional[str] = None
    testCaseType: Optional[int] = None

    def __str__(self):
        return self.model_dump_json(indent=4)