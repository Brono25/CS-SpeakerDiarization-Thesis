import torch

# Check if CUDA is available
if torch.cuda.is_available():
    print("CUDA is available!")
    print("PyTorch is using:", torch.cuda.get_device_name())
else:
    print("CUDA is not available. PyTorch is using CPU.")
