import numpy as np
import json
import csv


def load_data(dataPath):
    """
    加载数据
    :param dataPath: 数据路径
    :return: 标签
    """
    with open(dataPath, 'r', encoding='utf-8') as f:
        JsonData = f.read()
    data = json.loads(JsonData)
    roomdatalist = []
    roompricelist = []
    for roomdata in data[:-100]:
        roomlist = []
        pricelist = []
        for i, j in roomdata.items():
            if i == 'pageNum' or i == 'price_location':
                pass
            else:
                roomlist.append(float(j))
        roomdatalist.append(roomlist)
        roompricelist.append(pricelist)
    X_label = np.array(roomdatalist)
    Y_label = np.array(roompricelist)

    roomdatalist_test = []
    roompricelist_test = []
    for roomdata in data[-100:]:
        roomlist_test = []
        pricelist_test = []
        for i, j in roomdata.items():
            if i == 'pageNum' or i == 'price_location':
                pass
            else:
                roomlist_test.append(float(j))
        roomdatalist_test.append(roomlist_test)
        roompricelist_test.append(pricelist_test)
    X_label_test = np.array(roomdatalist_test)
    Y_label_test = np.array(roompricelist_test)

    return X_label, X_label_test


def readData(filePath="X_label.csv"):
    """
    读取数据
    :return:
    """
    X = []
    y = []
    with open(filePath) as f:
        rdf = csv.reader(f)
        for line in rdf:
            xline = [1.0]
            for s in line[:-1]:  # line[:-1]是除去价格那一行
                xline.append(float(s))
            X.append(xline)  # X包含条件因素
            y.append(float(line[-1]))  # 最终价格
    return X, y


def featureNormalize(X):
    X_norm = X
    mu = np.zeros((1, X.shape[1]))
    sigma = np.zeros((1, X.shape[1]))
    for i in range(X.shape[1]):
        mu[0, i] = np.mean(X[:, i])  # 均值
        sigma[0, i] = 1 if np.std(X[:, i]) == 0 else np.std(X[:, i])  # 标准差
    X_norm = (X - mu) / sigma
    return X_norm, mu, sigma


# 计算损失
def computeCost(X, y, theta):
    m = y.shape[0]
    #     J = (np.sum((X.dot(theta) - y)**2)) / (2*m)
    C = X.dot(theta) - y
    J2 = (C.T.dot(C)) / (2 * m)
    return J2


# 梯度下降
def gradientDescent(X, y, theta, alpha, num_iters):
    m = y.shape[0]
    # print(m)
    # 存储历史误差
    J_history = np.zeros((num_iters, 1))
    for iter in range(num_iters):
        # 对J求导，得到 alpha/m * (WX - Y)*x(i)， (3,m)*(m,1)  X (m,3)*(3,1) = (m,1)
        theta = theta - (alpha / m) * (X.T.dot(X.dot(theta) - y))
        J_history[iter] = computeCost(X, y, theta)
    return J_history, theta


def predict(data, real_price):
    testx = np.array(data)
    testx = ((testx - mu) / sigma)
    testx = np.hstack([testx, np.ones((testx.shape[0], 1))])
    price = testx.dot(theta)
    print('predit value is %f ,the real value is %f ' % (price, real_price))


if __name__ == '__main__':
    X_label, Y_label = readData()

    X_label = np.array(X_label, np.float64)  # 数据是浮点型
    Y_label = np.array(Y_label, np.float64)  # 数据是浮点型
    Y_label = Y_label.reshape(Y_label.shape[0], -1)
    # X_label.shape = (2671, 10)
    # Y_label.shape = (2671, 1)

    iterations = 10000  # 迭代次数
    alpha = 0.01  # 学习率
    m = Y_label.shape[0]
    x, mu, sigma = featureNormalize(X_label)
    X = np.hstack([x, np.ones((x.shape[0], 1))])
    # X = X[range(2),:]
    # y = y[range(2),:]

    theta = np.zeros((11, 1))

    j = computeCost(X, Y_label, theta)
    J_history, theta = gradientDescent(X, Y_label, theta, alpha, iterations)

    print('Theta found by gradient descent', theta)

    X_label_test, Y_label_test = readData('X_label_test.csv')
    for i, j in zip(X_label_test, Y_label_test):
        predict(i, j)
