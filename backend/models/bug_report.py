from pydantic import BaseModel

class BugReport(BaseModel):

    title: str

    description: str

    severity: str