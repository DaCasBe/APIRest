import math
from fastapi import APIRouter

from core.schemas.schema import MathsLeastCommonMultiple, MathsPlusOne

router = APIRouter(prefix="/maths", tags=["maths"])


@router.get("/numbers")
async def least_common_multiple(numbers: MathsLeastCommonMultiple):
    lcm = numbers.numbers[0]

    for number in numbers.numbers:
        lcm = lcm*number//math.gcd(lcm, number)

    return {"message": f"The least common multiple is {lcm}"}


@router.get("/number")
async def plus_one(number: MathsPlusOne):
    return {"message": f"{number.number+1}"}
