import Cla2
import torch.nn as nn
import torch.nn.functional as F



class Digit(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 10, 5)
        self.conv2 = nn.Conv2d(10, 20, 3)
        self.fc1 = nn.Linear(20 * 28 * 12, 500)
        self.fc2 = nn.Linear(500, 9)

    def forward(self, x):
        input_size = x.size(0)
        x = self.conv1(x)
        # 64-5+1=60 32-5+1=28 output=10*60*28
        x = F.relu(x)
        x = F.max_pool2d(x, 2, 2)
        # output=10*30*14

        x = self.conv2(x)
        # 30-3+1=28 14-3+1=12 output=20*28*12
        x = F.relu(x)

        x = x.view(input_size, -1)
        # 拉伸20*28*12=6720

        x = self.fc1(x)
        x = F.relu(x)

        x = self.fc2(x)

        output = F.log_softmax(x, dim=1)
        return output


fenlei = Cla2.Fenlei()
list1 = fenlei.classify()
print(list1)
