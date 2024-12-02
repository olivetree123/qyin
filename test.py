from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

from qyin import (
    Qyin,
    Route,
    RouteGroup,
)


class PingRequest(BaseModel):
    """Ping Request"""
    req_foo: str = Field(description="foo value of the request")
    req_bar: str = Field(description="bar value of the request")


class PingResponse(BaseModel):
    """Ping response"""
    resp_foo: str = Field(description="foo value of the response")
    resp_bar: str = Field(description="bar value of the response")


async def home(request):
    return JSONResponse("Homepage")


root_router = RouteGroup(path="/",
                    routes=[
                        Route.get("/", home, response_ok=PingResponse),
                        Route.post("/ping",
                                   home,
                                   request_model=PingRequest,
                                   response_ok=PingResponse),
                    ])

user_router = RouteGroup(path="/user")
project_router = RouteGroup(path="/project")

user_router.post("/login",
                 home,
                 request_model=PingRequest,
                 response_ok=PingResponse)
project_router.post("/create",
                    home,
                    request_model=PingRequest,
                    response_ok=PingResponse)

root_router.add_router(user_router)
root_router.add_router(project_router)

qyin = Qyin(title="qying", description="qyin is a python web framework")
qyin.set_root_router(root_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(qyin, host="0.0.0.0", port=8000)
