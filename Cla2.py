import collections
import os

import torchvision
from torch.utils.data import DataLoader
from torchvision import transforms  # 进行训练数据的转换
import torch.nn as nn
import torch
import torch.nn.functional as F
import torch.optim as optim


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


class Fenlei:
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    BATCH_SIZE = 9999
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    EPOCH = 30

    # 要求我们的图像都在一个适当的目录结构中，其中每个目录分别是一个标签
    train_data_path = "./train/"
    test_data_path = "./test/"
    predict_data_path = "./pythonProject2/predict"
    # 设置转换的各项参数
    transforms = transforms.Compose([transforms.Resize((64, 32)),  # 将每个图片都缩放为相同的分辨率64x64，便于GPU的处理
                                     transforms.Grayscale(num_output_channels=1),
                                     transforms.ToTensor(),  # 将数据集转化为张量
                                     transforms.Normalize((0.1307,), (0.3081,))  # 设置用于归一化的参数
                                     ])
    # 处理训练数据集
    train_data = torchvision.datasets.ImageFolder(root=train_data_path, transform=transforms)
    test_data = torchvision.datasets.ImageFolder(root=test_data_path, transform=transforms)
    predict_data = ""
    try:
        predict_data = torchvision.datasets.ImageFolder(root=predict_data_path, transform=transforms)
    except:
        pass
    train_loader = DataLoader(train_data, batch_size=BATCH_SIZE, shuffle=True)
    test_loader = DataLoader(test_data, batch_size=BATCH_SIZE, shuffle=False)
    predict_loader = DataLoader(predict_data, batch_size=BATCH_SIZE, shuffle=False)

    model = Digit().to(DEVICE)
    optimizer = optim.Adam(model.parameters())

    def train_model(self, model, device, train_loader, optimizer, epoch):
        model.train()
        for batch_index, (data, target) in enumerate(train_loader):
            data, target = data.to(device), target.to(device)
            optimizer.zero_grad()
            output = model(data)
            print(output)
            print(target)
            loss = F.cross_entropy(output, target)
            loss.backward()
            optimizer.step()
            if batch_index % 3000 == 0:
                print("Train Epoch : {} \t Loss : {:.6f}".format(epoch, loss.item()))

    def test_model(self, model, device, test_loader):
        model.eval()
        correct = 0.0
        test_loss = 0.0

        with torch.no_grad():
            for data, target in test_loader:
                data, target = data.to(device), target.to(device)
                output = model(data)
                print(output)
                print(target)
                # out = torch.sort(output, descending=True)
                test_loss += F.cross_entropy(output, target).item()
                softout = F.softmax(output, dim=1)
                print(softout)
                pred = output.max(1, keepdim=True)[1]
                print(pred)
                correct += pred.eq(target.view_as(pred)).sum().item()
                pred = softout.max(1, keepdim=True)
                print(pred)
            test_loss /= len(test_loader.dataset)
            print("Test Average loss : {:.4f}, Accuracy : {:.3f}\n".format(test_loss,
                                                                           100.0 * correct / len(test_loader.dataset)))

    def read_file(self, path1):
        filelist1 = os.listdir(path1)
        file_image = [file for file in filelist1 if file.endswith('.png')]
        return file_image

    def classify(self):
        # for epoch in range(1, EPOCH + 1):
        #     train_model(model, DEVICE, train_loader, optimizer, epoch)
        #
        # torch.save(model, "./model.pt")
        model = torch.load("./model.pt")
        self.test_model(model, self.DEVICE, self.test_loader)
        taxingfanzhuan = {}
        toujiandi = {}
        v = {}
        w = {}
        taxingfanzhuanOut = {}
        toujiandiOut = {}
        vOut = {}
        wOut = {}
        filelist = self.read_file("./pythonProject2/predict/picture")
        for i in range(len(filelist)):
            filelist[i] = filelist[i][0:6]
        for data1, _ in self.predict_loader:
            output1 = model(data1)
            softout1 = F.softmax(output1, dim=1)
            # out = torch.sort(output, descending=True)
            pred1 = output1.max(1, keepdim=True)[1]
            pred1 = softout1.max(1, keepdim=True)
            values = pred1[0]
            indices = pred1[1]
            for i in range(len(values)):
                if indices[i] == 0:
                    taxingfanzhuan[filelist[i]] = values[i].item()
                elif indices[i] == 1:
                    toujiandi[filelist[i]] = values[i].item()
                elif indices[i] == 2:
                    v[filelist[i]] = values[i].item()
                elif indices[i] == 3:
                    w[filelist[i]] = values[i].item()
        ta = sorted(taxingfanzhuan.items(), key=lambda x: x[1], reverse=True)
        print(ta)
        for i in range(int(len(ta) / 2)):
            taxingfanzhuanOut[ta[i][0]] = ta[i][1]
        print(taxingfanzhuanOut)
        tou = sorted(toujiandi.items(), key=lambda x: x[1], reverse=True)
        print(tou)
        for i in range(int(len(tou) / 2)):
            toujiandiOut[tou[i][0]] = tou[i][1]
        print(toujiandiOut)
        vi = sorted(v.items(), key=lambda x: x[1], reverse=True)
        print(vi)
        for i in range(int(len(vi) / 2)):
            vOut[vi[i][0]] = vi[i][1]
        print(vOut)
        w1 = sorted(w.items(), key=lambda x: x[1], reverse=True)
        print(w1)
        for i in range(int(len(w1) / 2)):
            wOut[w1[i][0]] = w1[i][1]
        print(wOut.keys())
        return list(vOut.keys()), list(wOut.keys()), list(toujiandiOut.keys()), list(taxingfanzhuanOut.keys())
