import flwr as fl
from flwr.server import ServerConfig

def start_server():
    config = ServerConfig(num_rounds=3)
    fl.server.start_server(server_address="0.0.0.0:8081", config=config)

if __name__ == '__main__':
    start_server()
