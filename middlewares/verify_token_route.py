from fastapi import Request
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from helpers.functions import validateToken

class VerifyTokenRoute(APIRoute):
    def get_route_handler(self):
        original_route = super().get_route_handler()

        async def verify_token_middleware(request: Request):
            if "authorization" not in request.headers:
                return JSONResponse(content={"auth": False}, status_code=403)

            token = request.headers['authorization']
            # print(token)

            validToken = validateToken(token)

            if validToken:
                return await original_route(request)
            else:
                return JSONResponse(content={"auth": False}, status_code=403)
    
        return verify_token_middleware