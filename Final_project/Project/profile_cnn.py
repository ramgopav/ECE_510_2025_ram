import cProfile
import pstats
import torch
from train_char_cnn import model, train_loader, device

# Load a batch (in memory, no file I/O)
images, labels = next(iter(train_loader))
images, labels = images.to(device), labels.to(device)

def run_forward_pass():
    model.eval()
    with torch.no_grad():
        output = model(images)  # Just forward pass

# Profile forward pass only
cProfile.run('run_forward_pass()', 'profile_results.prof')

# Save summary
with open("profile_summary.txt", "w") as f:
    ps = pstats.Stats("profile_results.prof", stream=f)
    ps.strip_dirs().sort_stats("cumulative").print_stats(25)
