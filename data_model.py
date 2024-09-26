from datetime import datetime
from pydantic import BaseModel, FieldValidationInfo, field_validator, ConfigDict
from enum import Enum

# Define the Speaker Enum
class Speaker(str, Enum):
    INTERVIEWER = "INTERVIEWER"
    INTERVIEWEE = "INTERVIEWEE"

# Define the Transcription model
class Transcription(BaseModel):
    speaker: Speaker
    transcription: str
    timestamp: str

    model_config = ConfigDict(use_enum_values=True) 

    # Custom validator for timestamp using Pydantic V2 style
    @field_validator('timestamp')
    def validate_timestamp(cls, value: str, info: FieldValidationInfo):
        try:
            # Validate the timestamp format as HH:MM:SS
            datetime.strptime(value, '%H:%M:%S')
        except ValueError:
            raise ValueError('timestamp must be in the format HH:MM:SS')
        return value

# Define the Transcriptions list
class Transcriptions(BaseModel):
    transcriptions: list[Transcription]
    model_config = ConfigDict(use_enum_values=True) 