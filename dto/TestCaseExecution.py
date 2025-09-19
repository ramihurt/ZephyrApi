from __future__ import annotations
from dataclasses import dataclass
from typing import List
from .TestCaseStatus import TestCaseStatus
from typing import Optional, Any
from pydantic import BaseModel, ConfigDict

class TestCaseExecution(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    id: Optional[str] = None
    issueId: Optional[int] = None
    versionId: Optional[int] = None
    projectId: Optional[int] = None
    cycleId: Optional[str] = None
    orderId: Optional[int] = None
    createdBy: Optional[str] = None
    createdByAccountId: Optional[str] = None
    testCaseStatus: Optional[TestCaseStatus] = None
    cycleName: Optional[str] = None
    assignedTo: Optional[str] = None
    assignedToAccountId: Optional[str] = None
    defects: Optional[List[Any]] = None
    stepDefects: Optional[List[Any]] = None
    executionDefectCount: Optional[int] = None
    stepDefectCount: Optional[int] = None
    totalDefectCount: Optional[int] = None
    creationDate: Optional[str] = None
    executedByZapi: Optional[bool] = None
    assignedOn: Optional[str] = None
    folderId: Optional[str] = None
    folderName: Optional[str] = None
    zfjIndexType: Optional[str] = None
    issueTypeId: Optional[int] = None
    projectType: Optional[str] = None
    issueIndex: Optional[int] = None
    projectCycleVersionIndex: Optional[str] = None
    executionStatusIndex: Optional[int] = None
    projectIssueCycleVersionIndex: Optional[str] = None

    def __str__(self):
        return self.model_dump_json(indent=4)