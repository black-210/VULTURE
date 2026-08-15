import pytest

pytest.importorskip('torch')
import torch
from torch import nn
from torch.utils.data import TensorDataset
from vulture.ml.torch_trainer import TorchTrainer


def test_torch_trainer_smoke():
    # small linear regression
    X = torch.randn(100, 4)
    y = torch.randn(100, 1)
    ds = TensorDataset(X, y)
    model = nn.Sequential(nn.Linear(4, 16), nn.ReLU(), nn.Linear(16, 1))
    opt = torch.optim.SGD(model.parameters(), lr=0.01)
    loss_fn = nn.MSELoss()
    trainer = TorchTrainer(model, opt, loss_fn, device='cpu')
    hist = trainer.fit(ds, epochs=1, batch_size=16)
    assert 'train_loss' in hist
