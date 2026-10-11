from pydantic import BaseModel, Field
from typing import Literal

class SupportTicket(BaseModel):
    category: Literal["Billing", "Technical", "General Inquiry"]
    description: str = Field(description="A brief description of the support ticket")
    priority: Literal["Low", "Medium", "High"] = Field(description="The priority level of the support ticket")
    summary: str = Field(description="A brief summary of the support ticket")
    requires_human_review: bool = Field(description="Indicates if the support ticket requires human review")
