from fastapi import APIRouter  
  
from api.routes.routes import router as get_examples  

router = APIRouter()  
  
router.include_router(get_examples)
