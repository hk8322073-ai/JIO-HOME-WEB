from pydantic import BaseModel, Field, field_validator

class OTPRequest(BaseModel):
    mobileNum: str = Field(
        ...,
        min_length=13,
        max_length=13,
        description="Mobile number in format +91XXXXXXXXXX"
    )
    
    @field_validator('mobileNum')
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        """Validate mobile number format."""
        if not v.startswith('+91'):
            raise ValueError('Mobile must start with +91')
        if len(v) != 13:
            raise ValueError('Mobile must be exactly 13 characters (e.g., +919876543210)')
        if not v[1:].isdigit():
            raise ValueError('Mobile must contain only digits after +91')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {"mobileNum": "+919876543210"}
        }

    
class OTPVerify(BaseModel):
    mobileNum: str = Field(
        ...,
        min_length=13,
        max_length=13,
        description="Mobile number in format +91XXXXXXXXXX"
    )
    otp: str = Field(
        ...,
        min_length=6,
        max_length=6,
        description="6-digit OTP"
    )
    
    @field_validator('mobileNum')
    @classmethod
    def validate_mobile(cls, v: str) -> str:
        """Validate mobile number format."""
        if not v.startswith('+91'):
            raise ValueError('Mobile must start with +91')
        if len(v) != 13:
            raise ValueError('Mobile must be exactly 13 characters')
        if not v[1:].isdigit():
            raise ValueError('Mobile must contain only digits after +91')
        return v
    
    @field_validator('otp')
    @classmethod
    def validate_otp(cls, v: str) -> str:
        """Validate OTP format."""
        if not v.isdigit():
            raise ValueError('OTP must contain only digits')
        if len(v) != 6:
            raise ValueError('OTP must be exactly 6 digits')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {"mobileNum": "+919876543210", "otp": "123456"}
        }
    
class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(
        ...,
        min_length=1,
        description="Refresh token from login response"
    )
    token_identifier: str = Field(
        ...,
        min_length=1,
        description="Token identifier from login response"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "refresh_token": "your_refresh_token_here",
                "token_identifier": "your_token_identifier_here"
            }
        }