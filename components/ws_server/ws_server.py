from overrides import final, override
from simple_websocket_server import WebSocketServer
from structures import ReusableThread, WsMessage
from .types import WebsocketClient, websocket_clients


class WsServer(ReusableThread):
    def __init__(self, host: str = "127.0.0.1", port: int = 8080):
        self.__server = WebSocketServer(host, port, WebsocketClient)

        ReusableThread.__init__(self)

    @final
    @override
    def _run_after_loop(self) -> None:
        self.__server.close()

    @final
    @override
    def _thread_loop(self) -> None:
        self.__server.handle_request()

    def broadcast(self, message: WsMessage):
        if self._is_running:
            for client in websocket_clients:
                client.send_message(str(message))
        else:
            raise Exception("Server is not running")
