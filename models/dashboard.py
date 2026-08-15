from pydantic import BaseModel, Field, field_validator

class CustomerLocationPayload(BaseModel):
    customerId: str = Field(
        ...,
        min_length=1,
        description="Customer ID"
    )
    locationId: str = Field(
        ...,
        min_length=1,
        description="Location ID"
    )
    
    @field_validator('customerId', 'locationId')
    @classmethod
    def validate_ids(cls, v: str) -> str:
        """Validate that IDs are not empty."""
        if not v or v.isspace():
            raise ValueError('ID cannot be empty')
        return v.strip()
    
    class Config:
        json_schema_extra = {
            "example": {
                "customerId": "CUST123456",
                "locationId": "LOC789012"
            }
        }