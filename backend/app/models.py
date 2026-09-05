from pydantic import BaseModel, Field
from typing import Optional

class AnalyzeRequest(BaseModel):
    merchant: str = "NovaKart"
    payment_success_rate: float = Field(91.2, ge=0, le=100)
    baseline_success_rate: float = Field(97.8, ge=0, le=100)
    transactions_per_hour: int = Field(1200, ge=0)
    average_order_value: float = Field(1850, ge=0)

class PolicyRequest(BaseModel):
    confidence: float = Field(..., ge=0, le=1)
    action_value: float = Field(..., ge=0)
    high_risk: bool = False
    auto_actions_enabled: bool = True
    minimum_confidence: float = 0.90
    maximum_automatic_action_value: float = 10000

class ExecuteRequest(BaseModel):
    approved: bool
    action: str
    merchant: str = "NovaKart"

class VerifyRequest(BaseModel):
    before_success_rate: float
    after_success_rate: float
    expected_after_success_rate: float = 97.1
    tolerance: float = 0.5
