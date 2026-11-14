from pydantic import Field, BaseModel

class StandUpUpdate(BaseModel):
    
    yesterday: str = Field(description="Bullet point of completed tasks and yesterday's meetings")
    
    today: str = Field(description="Bullet point of 'In Progress' tasks and today's meetings")
    
    blockers: str = Field(description="Any blockers identified in the text. If no blockers exists write 'None'.")