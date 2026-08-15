"""PyTorch GPU training support."""

import numpy as np
import logging

logger = logging.getLogger(__name__)

HAS_TORCH = False

try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
    from torch.utils.data import DataLoader, TensorDataset
    HAS_TORCH = True
except ImportError:
    pass


class GPUTrainer:
    """PyTorch-based GPU training."""

    def __init__(self):
        if not HAS_TORCH:
            raise ImportError("PyTorch required. Install: pip install torch")
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        logger.info(f"Using device: {self.device}")
        self.model = None
        self.optimizer = None
        self.loss_fn = None

    def create_mlp(self, input_size: int, hidden_sizes: list, output_size: int) -> None:
        """Create MLP model.
        
        Args:
            input_size: Input dimension
            hidden_sizes: Hidden layer sizes
            output_size: Output dimension
        """
        layers = [nn.Linear(input_size, hidden_sizes[0]), nn.ReLU()]
        for i in range(len(hidden_sizes) - 1):
            layers.extend([
                nn.Linear(hidden_sizes[i], hidden_sizes[i+1]),
                nn.ReLU(),
                nn.Dropout(0.2)
            ])
        layers.append(nn.Linear(hidden_sizes[-1], output_size))
        
        self.model = nn.Sequential(*layers).to(self.device)
        logger.info(f"Created MLP with hidden layers: {hidden_sizes}")

    def train_epoch(self, train_loader: DataLoader, learning_rate: float = 0.001) -> float:
        """Train one epoch.
        
        Args:
            train_loader: DataLoader
            learning_rate: Learning rate
            
        Returns:
            Average loss
        """
        if self.model is None:
            raise RuntimeError("Model not created")
        
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.loss_fn = nn.CrossEntropyLoss()
        
        self.model.train()
        total_loss = 0
        
        for X_batch, y_batch in train_loader:
            X_batch = X_batch.to(self.device)
            y_batch = y_batch.to(self.device)
            
            self.optimizer.zero_grad()
            outputs = self.model(X_batch)
            loss = self.loss_fn(outputs, y_batch)
            loss.backward()
            self.optimizer.step()
            
            total_loss += loss.item()
        
        avg_loss = total_loss / len(train_loader)
        logger.debug(f"Epoch loss: {avg_loss:.4f}")
        return avg_loss

    def predict(self, X: np.ndarray) -> np.ndarray:
        """Make predictions.
        
        Args:
            X: Input data
            
        Returns:
            Predictions
        """
        if self.model is None:
            raise RuntimeError("Model not created")
        
        self.model.eval()
        X_tensor = torch.from_numpy(X).float().to(self.device)
        
        with torch.no_grad():
            outputs = self.model(X_tensor)
        
        return outputs.cpu().numpy()
