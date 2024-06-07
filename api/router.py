from fastapi import APIRouter, HTTPException, status
from shemas.shemas import Example

router = APIRouter()


# Only an example
fake_db = [
    {"name": "Foo Fighters", "song": "My Hero"},
    {"name": "Metallica", "song": "Hero of the Day"}
]


@router.get(
    "/examples",
    response_model=list[Example],
    status_code=status.HTTP_200_OK,
)
async def get_examples() -> list[Example]:
    return [Example(**ex)for ex in fake_db]


@router.get("/status/200")
async def status_200():
    return {"status": "OK"}


@router.get("/status/403")
async def status_403():
    raise HTTPException(status_code=403, detail="Forbidden")


@router.get("/status/404")
async def status_404():
    raise HTTPException(status_code=404, detail="Not Found")


@router.get("/status/500")
async def status_500():
    raise HTTPException(status_code=500, detail="Internal Server Error")
