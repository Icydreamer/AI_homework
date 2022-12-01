import numpy as np
import matplotlib.pyplot as plt


# 随机生成nums个城市数据
def city_generator(nums):
    from numpy import random

    citys = []
    N = 0
    while N < nums:
        x = random.randn()
        y = random.randn()
        if [x, y] not in citys:
            citys.append([x, y])
            N = N + 1
    return np.array(citys)


# CITY-52,包含52个城市
def init_city52():
    citys = np.array([[565.0, 575.0], [25.0, 185.0], [345.0, 750.0], [945.0, 685.0], [845.0, 655.0],
                      [880.0, 660.0], [25.0, 230.0], [525.0, 1000.0], [580.0, 1175.0], [650.0, 1130.0],
                      [1605.0, 620.0], [1220.0, 580.0], [1465.0, 200.0], [1530.0, 5.0], [845.0, 680.0],
                      [725.0, 370.0], [145.0, 665.0], [415.0, 635.0], [510.0, 875.0], [560.0, 365.0],
                      [300.0, 465.0], [520.0, 585.0], [480.0, 415.0], [835.0, 625.0], [975.0, 580.0],
                      [1215.0, 245.0], [1320.0, 315.0], [1250.0, 400.0], [660.0, 180.0], [410.0, 250.0],
                      [420.0, 555.0], [575.0, 665.0], [1150.0, 1160.0], [700.0, 580.0], [685.0, 595.0],
                      [685.0, 610.0], [770.0, 610.0], [795.0, 645.0], [720.0, 635.0], [760.0, 650.0],
                      [475.0, 960.0], [95.0, 260.0], [875.0, 920.0], [700.0, 500.0], [555.0, 815.0],
                      [830.0, 485.0], [1170.0, 65.0], [830.0, 610.0], [605.0, 625.0], [595.0, 360.0],
                      [1340.0, 725.0], [1740.0, 245.0]])
    return citys


class TSP:

    def __init__(self):
        self._init_citys()
        self._init_dist()
        self._init_params()

    # 初始化参数
    def _init_params(self):
        # 初始温度
        self.T = 280
        # 每个温度下的迭代次数
        self.L = 100 * self.n
        # 温度下降缩减因子
        self.alpha = 0.92
        # 初始状态
        self.S = np.arange(self.n)

    # 初始化城市
    def _init_citys(self):
        self.citys = init_city52()
        # self.citys = city_generator(30)
        self.n = self.citys.shape[0]

    # 得到距离矩阵的函数
    def _init_dist(self):
        self.Dist = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(i, self.n):
                self.Dist[i][j] = self.Dist[j][i] = np.linalg.norm(self.citys[i] - self.citys[j])

    # 计算在状态下S的能量
    def energy(self, S):
        sum = 0
        for i in range(self.n - 1):
            sum = sum + self.Dist[S[i]][S[i + 1]]
        sum = sum + self.Dist[S[self.n - 1]][S[0]]
        return sum

    # 从状态S的邻域中随机选择
    def neighbors(self, S):
        S_neibor = np.copy(S)
        u = np.random.randint(0, self.n)
        v = np.random.randint(0, self.n)
        while u == v:
            v = np.random.randint(0, self.n)
        S_neibor[u], S_neibor[v] = S_neibor[v], S_neibor[u]
        return S_neibor

    # 从状态S的邻域中随机选择
    def neighbors2(self, S):
        S_neibor = np.copy(S)
        u = np.random.randint(0, self.n)
        v = np.random.randint(0, self.n)
        if u > v:
            u, v = v, u
        while u == v:
            v = np.random.randint(0, self.n)
        temp = S_neibor[u:v]
        S_neibor[u:v] = temp[::-1]
        return S_neibor

    # 模拟退火搜索过程
    def search(self):
        Ts = []
        Es = []
        while self.T >= 0.1:
            print('search on T:{}'.format(self.T))
            for i in range(self.L):
                E_pre = self.energy(self.S)
                S_now = self.neighbors2(self.S)
                E_now = self.energy(S_now)
                if (E_now < E_pre) or (np.exp((E_pre - E_now) / self.T) >= np.random.rand()):
                    self.S = S_now

            Ts.append(self.T)
            E_now = self.energy(self.S)
            Es.append(E_now)
            print(E_now)

            # 判断是否达到终止状态
            self.T = self.T * self.alpha
        print(self.S)
        print('finished\n')

        return Ts, Es


if __name__ == '__main__':
    tsp = TSP()
    Ts, Es = tsp.search()
    plt.plot(Es)
    plt.show()