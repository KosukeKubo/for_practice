import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np

X = np.random.rand(1000, 10)
y = np.random.randint(0, 2, 1000)

def train_pipeline(X, y):
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2)
    
    # テンソル変換
    X_train = torch.FloatTensor(X_train)
    y_train = torch.LongTensor(y_train)
    
    # シンプルなモデル
    model = nn.Sequential(
        nn.Linear(10, 50),
        nn.ReLU(),
        nn.Linear(50, 2)
    )
    
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    
    # 学習ループ
    epochs = 10
    for epoch in range(epochs):
        
        outputs = model(X_train)
        loss = criterion(outputs, y_train)
        
        loss.backward()
        optimizer.step()
        
        if epoch % 2 == 0:
            print(f"Epoch {epoch}, Loss: {loss}") 


    test_outputs = model(torch.FloatTensor(X_test))
    _, predicted = torch.max(test_outputs, 1)
    
    accuracy = (predicted == torch.LongTensor(y_test)).sum().item() / len(y_test)
    print(f"Test Accuracy: {accuracy}")

if __name__ == "__main__":
    train_pipeline(X, y)