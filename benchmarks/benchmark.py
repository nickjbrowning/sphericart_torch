import torch
import torch_sh
import time
torch.set_default_dtype(torch.float64)
from torch.profiler import profile

device = "cpu"

x = torch.rand((200000,), device=device, requires_grad=True)
y = torch.rand((200000,), device=device, requires_grad=True)
z = torch.rand((200000,), device=device, requires_grad=True)

l_max = 10

print("Forward pass")
start_time = time.time()
torch_sh.SphericalHarmonics.initialize("cpu", forward_gradients=False)
sh = torch_sh.SphericalHarmonics.compute(l_max, x, y, z)
finish_time = time.time()
print(f"done in {finish_time-start_time} seconds")

dummy_loss = torch.zeros((1,), device=device)
for tensor in sh:
    dummy_loss += torch.sum(tensor)

print()
print("Backward pass")
start_time = time.time()
with profile() as prof:
    dummy_loss.backward()
finish_time = time.time()
print(f"done in {finish_time-start_time} seconds")

print()
print(prof.key_averages().table(sort_by="cpu_time_total", row_limit=20))
