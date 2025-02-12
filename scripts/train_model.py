import torch.nn as nn
import torch

class FormationPredictor(nn.Module):
    def __init__(self):
        super(FormationPredictor, self).__init__()
        self.lstm = nn.LSTM(input_size=2, hidden_size=50, batch_first=True)
        self.fc = nn.Linear(50, 3)  # Assuming 3 formations

    def forward(self, x):
        x, _ = self.lstm(x)
        x = self.fc(x[:, -1, :])
        return x
