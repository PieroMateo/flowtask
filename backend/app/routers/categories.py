from fastapi import APIRouter, Depends

from app.dependencies import get_category_service
from app.schemas.category import CategoryRead
from app.services.category_service import CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("", response_model=list[CategoryRead])
def list_categories(service: CategoryService = Depends(get_category_service)):
    return service.list_categories()
