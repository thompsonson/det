from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List, Literal


class RiskDefinition(BaseModel):
    risk_statement: str = Field(
        ..., description="The original risk statement provided for analysis."
    )
    risk_description: str = Field(
        ...,
        description="A detailed description of the risk aligned with NIST RMF terminology.",
    )
    context: str = Field(
        ...,
        description="Relevant background information and identification of critical assets involved.",
    )
    risk_categorization: str = Field(
        ...,
        description="Classification of the risk based on NIST SP 800-60 guidelines.",
    )
    security_controls: List[str] = Field(
        ...,
        description="List of relevant NIST SP 800-53 controls associated with mitigating the risk.",
    )
    implementation_guidance: str = Field(
        ..., description="High-level suggestions for control implementation."
    )
    assessment_approach: str = Field(
        ..., description="Methods to evaluate control effectiveness."
    )
    risk_likelihood: Literal["Very Low", "Low", "Moderate", "High", "Very High"] = (
        Field(
            ...,
            description="Qualitative rating of the likelihood of the risk occurring.",
        )
    )
    risk_impact: Literal["Very Low", "Low", "Moderate", "High", "Very High"] = Field(
        ...,
        description="Qualitative rating of the impact of the risk, should it occur.",
    )
    authorization_recommendation: Literal["Accept", "Mitigate", "Transfer", "Avoid"] = (
        Field(..., description="Recommendation for risk treatment strategy.")
    )
    continuous_monitoring_strategy: str = Field(
        ..., description="Proposed ongoing risk management activities."
    )
