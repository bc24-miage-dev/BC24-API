from typing import List
from fastapi import APIRouter, HTTPException

from service.blockchain_service import BlockchainService
from service.walletService import PrivateKeyService
from shemas.RoleAssignmentRequest import RoleAssignmentRequest
from shemas.RoleResponse import RoleResponse

blockchainSerivce = BlockchainService()


private_key_service = PrivateKeyService()

router = APIRouter(
    prefix="/roles",
    tags=["roles"],
)


@router.get("/", response_model=List[str])
async def get_available_roles():
    try:
        return blockchainSerivce.get_available_roles()
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/{wallet_address}",
    response_model=RoleResponse,
    responses={400: {"description": "Bad Request"}},
)
async def get_role_of_wallet_address(wallet_address: str):
    try:
        roles = blockchainSerivce.get_role_of(wallet_address)
        return {"role": roles}
    except Exception as e:
        print(e)
        if str(e) == "Invalid wallet address":
            raise HTTPException(status_code=400, detail=str(e))

        raise HTTPException(status_code=500, detail={"error": str(e)})


@router.post("/assignRole")
async def assign_role_to_user(request: RoleAssignmentRequest):
    try:
        from_wallet_private_key = private_key_service.get_private_key(
            request.from_wallet_address
        )
        receit = (
            blockchainSerivce.assign_role_to_user(
                from_wallet_private_key=from_wallet_private_key,
                target_wallet_address=request.target_wallet_address,
                role=request.role,
            ),
        )

        return {"status": "Role assigned successfully"}
    except Exception as e:
        print(e)
        if str(e) == "Invalid wallet address":
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=500, detail=str(e))
