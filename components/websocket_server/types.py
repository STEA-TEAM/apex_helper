from overrides import final, override
from simple_websocket_server import WebSocket
from typing import List

websocket_clients = []


class WebsocketClient(WebSocket):
    @final
    @override
    def connected(self):
        print(self.address, "connected")
        for client in websocket_clients:
            client.send_message(self.address[0] + " - connected")
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


websocket_clients: List[WebsocketClient] = websocket_clients
