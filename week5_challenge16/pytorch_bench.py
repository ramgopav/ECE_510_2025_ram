#PyTorch reference & timing (1000 passes)
model = torch.nn.Sequential(
    torch.nn.Linear(4,5), torch.nn.ReLU(),
    torch.nn.Linear(5,1)
).to(device)
with torch.no_grad():
    model[0].weight.copy_(W1); model[0].bias.copy_(b1)
    model[2].weight.copy_(W2); model[2].bias.copy_(b2)

starter,ender=torch.cuda.Event(True),torch.cuda.Event(True)
reps=1000; torch.cuda.synchronize(); starter.record()
for _ in range(reps): y=model(x)
ender.record(); torch.cuda.synchronize()
print("PyTorch out %.6f | %.3f µs"%(y.item(),starter.elapsed_time(ender)*1000/reps))
