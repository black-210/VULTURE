"""
PyTorch Trainer utility for simple training loops with checkpointing and ONNX export.
Requires torch to be installed. The implementation is minimal and intended as a starting point.
"""
from typing import Any, Dict, Optional

try:
    import torch
    from torch import nn
    from torch.utils.data import DataLoader
except Exception:
    torch = None


class TorchTrainer:
    def __init__(self, model: Any, optimizer: Any, loss_fn: Any, device: Optional[str] = None):
        if torch is None:
            raise RuntimeError("torch is required for TorchTrainer")
        self.model = model
        self.optimizer = optimizer
        self.loss_fn = loss_fn
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def fit(self, dataset: Any, epochs: int = 1, batch_size: int = 32, val_dataset: Optional[Any] = None) -> Dict[str, Any]:
        loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
        history = {"train_loss": [], "val_loss": []}
        for epoch in range(epochs):
            self.model.train()
            total_loss = 0.0
            for xb, yb in loader:
                xb = xb.to(self.device)
                yb = yb.to(self.device)
                self.optimizer.zero_grad()
                preds = self.model(xb)
                loss = self.loss_fn(preds, yb)
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()
            avg_loss = total_loss / len(loader) if len(loader) else 0.0
            history["train_loss"].append(avg_loss)

            if val_dataset is not None:
                self.model.eval()
                vloader = DataLoader(val_dataset, batch_size=batch_size)
                vloss = 0.0
                with torch.no_grad():
                    for xb, yb in vloader:
                        xb = xb.to(self.device)
                        yb = yb.to(self.device)
                        preds = self.model(xb)
                        loss = self.loss_fn(preds, yb)
                        vloss += loss.item()
                history["val_loss"].append(vloss / len(vloader) if len(vloader) else 0.0)
        return history

    def save_checkpoint(self, path: str) -> None:
        torch.save(self.model.state_dict(), path)

    def load_checkpoint(self, path: str) -> None:
        self.model.load_state_dict(torch.load(path, map_location=self.device))

    def export_onnx(self, path: str, example_input: Any) -> bool:
        try:
            if not hasattr(self.model, "forward"):
                return False
            self.model.eval()
            torch.onnx.export(self.model, example_input.to(self.device), path)
            return True
        except Exception:
            return False
