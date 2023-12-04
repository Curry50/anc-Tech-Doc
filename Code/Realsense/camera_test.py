import sys
import torch
import os
from pathlib import Path
path = sys.argv[1]
path = os.path.abspath(path)
print(path)
model = torch.load(path)

