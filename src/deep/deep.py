# 导入必要库
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt


class NQueensProblem:
    """N皇后问题定义
    """

    def __init__(self, numOfQueens):
        self.numOfQueens = numOfQueens

    def __len__(self):
        """
        :return: the number of queens
        """
        return self.numOfQueens

    def getViolationsCount(self, positions):
        """
        计算给定解中的违规次数
        由于输入的每一行都包含唯一的列索引，因此行或列不可能违反约束，仅对角线需要计算违反约束数。
        """
        if len(positions) != self.numOfQueens:
            raise ValueError("size of positions list should be equal to ", self.numOfQueens)

        violations = 0

        # 遍历每对皇后，计算它们是否在同一对角线上:
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                # first queen in pair
                column1 = i
                row1 = positions[i]

                # second queen in pair
                column2 = j
                row2 = positions[j]

                if abs(column1 - column2) == abs(row1 - row2):
                    violations += 1

        return violations

    def plotBoard(self, positions):
        """
        根据给定的解在棋盘上绘制皇后的位置
        """

        if len(positions) != self.numOfQueens:
            raise ValueError("size of positions list must be equal to ", self.numOfQueens)

        fig, ax = plt.subplots()

        # 棋盘定义:
        board = np.zeros((self.numOfQueens, self.numOfQueens))
        # 棋盘颜色交替
        board[::2, 1::2] = 1
        board[1::2, ::2] = 1

        # 绘制棋盘
        ax.imshow(board, interpolation='none', cmap=mpl.colors.ListedColormap(['#ffc794', '#4c2f27']))

        # 读取棋子图片，并进行缩放
        queenThumbnail = plt.imread("queen-thumbnail.png")
        thumbnailSpread = 0.70 * np.array([-1, 1, -1, 1]) / 2

        # 棋子绘制
        for i, j in enumerate(positions):
            # 将棋子放在棋盘上
            ax.imshow(queenThumbnail, extent=[j, j, i, i] + thumbnailSpread)

        # 坐标轴设定
        ax.set(xticks=list(range(self.numOfQueens)), yticks=list(range(self.numOfQueens)))

        ax.axis('image')

        return plt