from typing import Any, Union

JsonData = Union[dict[str, JsonData], list[JsonData], str, int, bool]

class WebsocketCommunicator:
    scope: dict[str, Any]

    def __init__(self, asgi_application: object, resource: str) -> None: ...

    # connected, subprotocol
    async def connect(self) -> tuple[bool, object]: ...
    async def disconnect(self) -> None: ...
    async def send_json_to(self, data: JsonData) -> None: ...
    async def receive_json_from(self) -> JsonData: ...
    async def receive_nothing(self) -> bool: ...

    # From agiref.testing.ApplicationCommuniactor.receive_output
    async def receive_output(self, timeout: int = 1) -> dict[str, Any]: ...
