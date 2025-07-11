import flwr as fl
import torch
from peft import get_peft_model, LoraConfig, TaskType
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "tiiuae/falcon-7b-instruct",
    load_in_8bit=True,
    device_map="auto"
)

lora_config = LoraConfig(r=4, lora_alpha=16, task_type=TaskType.CAUSAL_LM, lora_dropout=0.05)
model = get_peft_model(model, lora_config)

class LoraFLClient(fl.client.NumPyClient):
    def get_parameters(self): return [val.cpu().numpy() for val in model.parameters()]
    def set_parameters(self, params): 
        for param, new_val in zip(model.parameters(), params): 
            param.data = torch.tensor(new_val)
    def fit(self, params, config): 
        self.set_parameters(params)
        return self.get_parameters(), 100, {}
    def evaluate(self, params, config): 
        self.set_parameters(params)
        return 0.5, 100, {}

if __name__ == '__main__':
    fl.client.start_numpy_client(server_address="localhost:8080", client=LoraFLClient())
