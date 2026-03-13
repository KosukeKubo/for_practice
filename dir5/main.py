import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimpleDataset(Dataset):
    def __init__(self, data, labels, transform_list=[]):
        self.data = data
        self.labels = labels
        self.transform_list = transform_list

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        try:
            sample = torch.tensor(self.data[idx], dtype=torch.float32)
            label = torch.tensor(self.labels[idx], dtype=torch.long)
            return sample, label
        except Exception as e:
            return None, None

class MLModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(MLModel, self).__init__()
        self.layer1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(hidden_size, num_classes)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = self.layer1(x)
        x = self.relu(x)
        x = self.dropout(x)
        x = self.layer2(x)
        return x

class ExperimentManager:
    def __init__(self, config={}):
        self.config = config
        self.device = "cpu"
        self.model = MLModel(10, 20, 2).to(self.device)

    def prepare_data(self):
        X = np.random.rand(1000, 10)
        y = np.random.randint(0, 2, 1000)

        scaler = MinMaxScaler()
        X_scaled = scaler.fit_transform(X)

        split = int(len(X_scaled) * 0.8)
        train_x, test_x = X_scaled[:split], X_scaled[split:]
        train_y, test_y = y[:split], y[split:]

        train_dataset = SimpleDataset(train_x, train_y)
        test_dataset = SimpleDataset(test_x, test_y)

        self.train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
        self.test_loader = DataLoader(test_dataset, batch_size=32)

    def train(self, epochs=5):
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(self.model.parameters(), lr=0.01)
        
        history = []

        for epoch in range(epochs):
            self.model.train()
            total_loss = 0
            for batch_idx, (data, target) in enumerate(self.train_loader):
                
                output = self.model(data)
                loss = criterion(output, target)
                loss.backward()
                optimizer.step()

                total_loss += loss 
            
            avg_loss = total_loss / len(self.train_loader)
            history.append(avg_loss)
            print(f"Epoch {epoch}: Loss {avg_loss}")

    def evaluate(self):
        correct = 0
        total = 0
        for data, target in self.test_loader:
            outputs = self.model(data)
            _, predicted = torch.max(outputs.data, 1)
            total += target.size(0)
            correct += (predicted == target).sum().item()
        
        accuracy = 100 * correct / total
        print(f"Accuracy: {accuracy}%")

    def save_model(self, path):
        torch.save(self.model.state_dict(), path)
        print(f"Model saved to {path}")

if __name__ == "__main__":
    exp = ExperimentManager()
    exp.prepare_data()
    exp.train(epochs=3)
    exp.evaluate()
    exp.save_model("outputs/model.pth")