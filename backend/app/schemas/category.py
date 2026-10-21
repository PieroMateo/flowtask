from pydantic import BaseModel, ConfigDict


# como se ve una categoria en las respuestas de la API
class CategoryRead(BaseModel):
    # permite armar el esquema directo desde el objeto de sqlalchemy
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
