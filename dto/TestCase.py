from __future__ import annotations

import json
from dataclasses import dataclass
from .TestCaseExecution import TestCaseExecution
from typing import Optional
from pydantic import BaseModel, ConfigDict


class TestCase(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    warningMessage: Optional[str] = None
    originMessage: Optional[str] = None
    execution: Optional[TestCaseExecution] = None
    issueKey: Optional[str] = None
    issueLabel: Optional[str] = None
    component: Optional[str] = None
    issueSummary: Optional[str] = None
    issueDescription: Optional[str] = None
    projectName: Optional[str] = None
    versionName: Optional[str] = None
    priority: Optional[str] = None
    priorityIconUrl: Optional[str] = None
    executionByDisplayName: Optional[str] = None
    assigneeType: Optional[str] = None
    assignedToDisplayName: Optional[str] = None
    testStepBeans: Optional[str] = None
    defectsAsString: Optional[str] = None
    projectKey: Optional[str] = None
    plannedExecutionTimeFormatted: Optional[str] = None
    actualExecutionTimeFormatted: Optional[str] = None
    executionWorkflowStatus: Optional[str] = None
    workflowLoggedTimedIncreasePercentage: Optional[str] = None
    workflowCompletePercentage: Optional[str] = None
    versionReleased: Optional[bool] = None
    customFieldValuesAsString: Optional[str] = None
    viewIssuePermission: Optional[bool] = None
    executionWorkflowEnabled: Optional[bool] = None

    def __str__(self):
        return self.model_dump_json(indent=4)