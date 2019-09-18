import numpy as np

"""
    如果异常点代表在商业中很重要的异常情况，并且需要被检测出来，则应选用MSE损失函数。
    相反，如果只把异常值当作受损数据，则应选用MAE损失函数。
"""


def loss_function_l1(x_label, y_label, w):
    """
            这是L1损失函数, 又称MAE损失函数
            是目标值与预测值之差的绝对值之和。
            如果训练数据被异常点所污染，那么MAE损失就更好用
            （比如，在训练数据中存在大量错误的反例和正例标记，但是在测试集中没有这个问题）。

            缺点：更新的梯度始终相同，也就是说，即使对于很小的损失值，
            梯度也很大。这样不利于模型的学习。为了解决这个缺陷，
            我们可以使用变化的学习率，在损失接近最小值时降低学习率。
    """
    loss = np.abs(np.dot(x_label, w) - y_label)
    return np.sum(loss)


def loss_function_l2(x_label, y_label, w):
    """
            这是L2损失函数, 又称MSE损失函数
            是目标值与预测值之差的平方之和。
            缺点：如果训练数据中异常点比较多, 则训练时会朝着减小异常误差点的方向更新，降低模型整体性能

            优点：即便使用固定的学习率也可以有效收敛。MSE损失的梯度随损失增大而增大，
            而损失趋于0时则会减小。这使得在训练结束时，使用MSE模型的结果会更精确。
    """
    loss = x_label.dot(w) - y_label

    return np.sum(loss**2)


def loss_function_huber(x_label, y_label, w, delta):
    """
        Huber损失函数
            使用MAE训练神经网络最大的一个问题就是不变的大梯度，
            这可能导致在使用梯度下降快要结束时，错过了最小点。
            而对于MSE，梯度会随着损失的减小而减小，使结果更加精确。
        优点：Huber损失结合了MSE和MAE的优点
        缺点：需要不断调整超参数delta
    """
    loss = np.where(np.abs(np.dot(x_label, w) - y_label) < delta, 0.5 * ((np.dot(x_label, w) - y_label) ** 2),
                    delta * np.abs(np.dot(x_label, w) - y_label) - 0.5 * (delta ** 2))
    return np.sum(loss)


def loss_function_log_cosh(x_label, y_label, w):
    """
    Log-Cosh损失函数
        对于较小的x，log(cosh(x))近似等于(x^2)/2，对于较大的x，近似等于abs(x)-log(2)。
        这意味着‘logcosh’基本类似于均方误差，但不易受到异常点的影响。
        它具有Huber损失所有的优点，但不同于Huber损失的是，Log-cosh二阶处处可微。
    """
    loss = np.log(np.cosh(np.dot(x_label, w) - y_label))
    return np.sum(loss)


def loss_function_quantile():
    """
        分位数损失函数
    """
    pass


if __name__ == '__main__':
    X_label = np.array([[1, 2, 3, 4], [3, 4, 5, 6], [5, 6, 7, 8], [7, 8, 9, 10]])
    Y_label = np.array([[5], [7], [9], [11]])
    print(X_label.shape, Y_label.shape)
    W = np.ones((X_label.shape[0], 0), dtype=np.float32)
    cost_1 = loss_function_l1(X_label, Y_label, W)
    cost_2 = loss_function_l2(X_label, Y_label, W)
    cost_3 = loss_function_huber(X_label, Y_label, W, 5)
    print(cost_1, cost_2, cost_3)