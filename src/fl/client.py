import flwr as fl
import torch
import torch.nn as nn
import numpy as np

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(2, 1)

    def forward(self, x):
        return self.fc(x)

model = Net()
X_train = np.random.rand(100, 2)
y_train = (X_train[:, 0] + X_train[:, 1] > 1).astype(float)

class FlowerClient(fl.client.NumPyClient):
    def get_parameters(self, config):  # Add 'config' here
        return [val.detach().cpu().numpy() for val in model.parameters()]

    def set_parameters(self, parameters):
        for param, new_val in zip(model.parameters(), parameters):
            param.data = torch.tensor(new_val)

    def fit(self, parameters, config):
        self.set_parameters(parameters)
        optimizer = torch.optim.SGD(model.parameters(), lr=0.1)
        for _ in range(5):
            optimizer.zero_grad()
            output = model(torch.tensor(X_train, dtype=torch.float32))
            loss = nn.MSELoss()(output.squeeze(), torch.tensor(y_train))
            loss.backward()
            optimizer.step()
        return self.get_parameters(config), len(X_train), {}

    def evaluate(self, parameters, config):
        self.set_parameters(parameters)
        return 0.5, len(X_train), {}


if __name__ == '__main__':
    fl.client.start_client(
        server_address="localhost:8081",
        client=FlowerClient().to_client()
    )
