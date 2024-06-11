from overrides import final, override
from pyautogui import size as get_screen_size
from simple_websocket_server import WebSocket
from structures import HandshakeServerMessage, ResultType, WsMessage
from typing import List

websocket_clients = []


class WebsocketClient(WebSocket):
    @final
    @override
    def connected(self):
        print(self.address, "connected")
        screen_size = get_screen_size()
        self.__send_ws_message(
            HandshakeServerMessage(
                {
                    "message": None,
                    "resolution": {
                        "height": screen_size.height,
                        "width": screen_size.width,
                    },
                    "result": ResultType.success,
                }
            )
        )
        websocket_clients.append(self)

    @final
    @override
    def handle(self):
        for client in websocket_clients:
            if client != self:
                client.send_message(self.address[0] + " - " + self.data)

    @final
    @override
    def handle_close(self):
        websocket_clients.remove(self)
        print(self.address, "closed")

    def __send_ws_message(self, message: WsMessage):
        self.send_message(str(message))


websocket_clients: List[WebsocketClient] = websocket_clients
