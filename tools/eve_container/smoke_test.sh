#!/bin/bash
# Container smoke test: verify the image (a) sees the GPU, (b) imports torch
# with sm_89 support, and (c) imports the EVE codebase with a tiny forward
# pass. This is *not* a full training run; it just proves the workaround is
# viable so a real run can be scheduled separately.
#
# Usage: ./tools/eve_container/smoke_test.sh

set -euo pipefail

cd "$(dirname "$0")"

CONTAINER_RUN="./run.sh"

echo "=== [1/3] torch + GPU visibility ==="
"${CONTAINER_RUN}" python -c "
import torch, sys
print('python', sys.version.split()[0])
print('torch', torch.__version__)
print('cuda available', torch.cuda.is_available())
print('device count', torch.cuda.device_count())
if torch.cuda.is_available():
    name = torch.cuda.get_device_name(0)
    cap  = torch.cuda.get_device_capability(0)
    print('device 0', name, 'cc', cap)
    assert cap >= (8, 9), f'expected sm_89, got {cap}'
    # Smoke kernel: forces JIT compilation against the installed CUDA arch
    # list. If sm_89 kernels are missing, the matmul below errors with
    # 'no kernel image is available for execution on the device'.
    a = torch.randn(2048, 2048, device='cuda')
    b = torch.randn(2048, 2048, device='cuda')
    c = (a @ b).sum().item()
    print('matmul ok (sum =', round(c, 2), ')')
"

echo
echo "=== [2/3] EVE module import ==="
"${CONTAINER_RUN}" python -c "
import sys
sys.path.insert(0, '/workspace/EVE')
from EVE import VAE_model
from utils import data_utils
print('VAE_model OK:', VAE_model.VAE_model)
print('data_utils OK:', data_utils.MSA_processing)
"

echo
echo "=== [3/3] tiny VAE forward/backward (10 steps, no MSA loaded) ==="
"${CONTAINER_RUN}" python -c "
import sys, json, torch
sys.path.insert(0, '/workspace/EVE')
from EVE import VAE_model

with open('/workspace/EVE/EVE/default_model_params.json') as f:
    params = json.load(f)

# Construct a minimal stand-in for the MSA data object that VAE_model.__init__
# inspects. The model only reads seq_len, alphabet_size, and Neff from this
# object during construction, so a tiny stub suffices for the forward/backward
# smoke test without touching real MSAs.
SEQ_LEN, ALPHABET_SIZE, BATCH = 30, 21, 64
StubData = type('StubData', (), dict(
    seq_len=SEQ_LEN, alphabet_size=ALPHABET_SIZE, Neff=float(BATCH),
))

model = VAE_model.VAE_model(
    model_name='smoke_test',
    data=StubData(),
    encoder_parameters=params['encoder_parameters'],
    decoder_parameters=params['decoder_parameters'],
    random_seed=42,
)
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = model.to(device)
print('model on', device, '— params:',
      sum(p.numel() for p in model.parameters()))

# Synthetic one-hot batch in the shape the encoder expects: (B, L, A).
# We do not need real MSA semantics; the point is to drive loss.backward()
# and optimizer.step() through the encoder/decoder so the hardened CUDA
# allocator and the upstream VAE graph are exercised together.
x = torch.randn(BATCH, SEQ_LEN, ALPHABET_SIZE, device=device)
opt = torch.optim.Adam(model.parameters(), lr=1e-4)
for step in range(10):
    opt.zero_grad()
    mu, log_var = model.encoder(x)
    z   = model.sample_latent(mu, log_var)
    px  = model.decoder(z)
    # px is a logits tensor of shape (B, L, A); use cross-entropy against the
    # arg-max of x as a stand-in target so the BCE term has a finite value.
    target = x.argmax(dim=-1)
    bce = torch.nn.functional.cross_entropy(
        px.reshape(-1, ALPHABET_SIZE), target.reshape(-1)
    )
    kld = -0.5 * (1 + log_var - mu.pow(2) - log_var.exp()).sum(dim=-1).mean()
    loss = bce + 1e-3 * kld
    loss.backward()
    opt.step()
    if step in (0, 9):
        print(f'  step {step:2d}  loss={loss.item():.4f}')

print('10-step forward/backward OK — container is viable for real training.')
"

echo
echo ">>> smoke_test.sh PASS"
