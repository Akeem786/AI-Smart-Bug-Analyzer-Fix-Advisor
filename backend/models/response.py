from pydantic import BaseModel

class AnalysisResponse(BaseModel):

    message: str

    similar_bugs: list