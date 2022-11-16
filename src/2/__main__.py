import copy
import numpy as np

path = '八皇后种群.txt'
f=open(path, 'w', encoding='UTF-8')
f.write('初始化种群为：\n')


def unfighting(sort):
    alist = list(set(sort))
    num = 0  # 初始化皇后冲突的对数为0
    # num=len(sort)-len(alist)   #求行上面冲突的的皇后个数

    # 求行上面冲突的的皇后对数
    x = []
    sort = list(sort)
    for i in range(len(alist)):
        x.append(sort.count(alist[i]))
    for i in x:
        if i >= 2:
            num = num + i * (i - 1) // 2
    # 求斜线上冲突的皇后的对数
    for i in range(n - 1):
        for j in range(i+1, n):
            if sort[i] - sort[j] == i - j or sort[i] - sort[j] == j-i :
                num = num + 1

    return int(n*(n-1)/2) - num


def drawchess(sort):

    chess = np.zeros((len(sort), len(sort)), dtype=int)
    # 创建八皇后棋盘
    for i in range(len(sort)):
        chess[sort[i]][i] = len(sort)
    for i in range(n):
        for j in range(n):
            if chess[i][j]==0:
                print('O',end='\t')
            else:
                print(chess[i][j],end='\t')
        print()


def FitFunction(sorts):
    # fits=np.zeros((len(sorts)),dtype=int)  #每个个体适应度初始化为0
    fits = []
    for sort in sorts:
        fits.append(unfighting(sort))

    if int(n*(n-1)//2) in fits:
        return fits
    sum = np.sum(fits)
    for i in range(len(sorts)):
        fits[i] = fits[i] / sum
    return fits


def discard(sorts):
    deepth.append(0)

    if len(deepth)==2800:
        print('超过了最大深度')
        return
    fits = FitFunction(sorts)
    f.write('第' + str(len(deepth)) + '代' + '\n')
    f.write(str(fits) + '\n')
    # 如果不打架的皇后个数为28则画出相应的棋盘
    if int(n*(n-1)//2) in fits:
        for y in fits:
            if y == int(n*(n-1)//2):
                print("优秀个体为：")
                print(sorts[fits.index(n*(n-1)//2)])
                print("棋盘为：")
                drawchess(sorts[fits.index(n*(n-1)//2)])

        return sorts

    new_sorts = []
    # 适应度低的终将被淘汰 在0.13~0.145之间随机产生一个数，适应度小于该数的会被淘汰
    miss = np.random.uniform(0.0130, 0.0145)
    for i in range(len(sorts)):
        if fits[i] > miss:
            new_sorts.append(sorts[i])

    # 保证新种群的个体数和旧种群数相同
    sub = len(sorts) - len(new_sorts)
    if sub > 0:
        if sub> int(np.ceil(len(sorts) * 0.3)):
            new_sorts.clear()
            # 将适应度低的个体淘汰掉 比例为25%
            for i in range(len(sorts)):
                sorts[i].append(fits[i])  # 将其对应的适应度以以匹配起来
            sorts.sort(key=lambda x: x[n], reverse=False)  # 按照适应度的高低排序:低到高
            indexstart = int(np.ceil(sub * 0.25))
            new_sorts=sorts[indexstart:]

        sub = len(sorts) - len(new_sorts)
        s = np.random.randint(0, len(new_sorts), sub)  #随机选择sub个位置上的个体数增加
        for x in s:
            new_sorts.insert(len(new_sorts)+1, new_sorts[x])

    np.random.shuffle(new_sorts)  # 随机打乱顺序
    Selection(new_sorts)


# 选择交叉变异函数  两两组合 用随机数产生交叉的位置
def Selection(sorts):
    fits = FitFunction(sorts)
    Len = len(sorts)
    new_sorts = copy.deepcopy(sorts)
    # 将适应度高的个体保留以保证子代的结果不会比父代差 比例为5%
    for i in range(Len):
        new_sorts[i].append(fits[i])  # 将其对应的适应度以以匹配起来
    new_sorts.sort(key=lambda x: x[8], reverse=True)  # 按照适应度的高低排序
    indexstart = int(np.ceil(Len * 0.05))
    del new_sorts[indexstart:]

    # 将保留的高适应度的个体从要进行交叉互换的队列里面删除
    for x in new_sorts:
        del x[8:]
        sorts.remove(x)

    # 交叉互换
    corssindex = np.random.randint(0, n, size=len(sorts) // 2)  # 随机产生每对交叉互换的位置
    for i in range(len(sorts) // 2):
        new1 = []
        new2 = []
        for x in sorts[2 * i][:corssindex[i]] :
            new1.append(x )
        for x in sorts[2 * i + 1][corssindex[i]:]:
            new1.append(x )
        for x in sorts[2 * i + 1][:corssindex[i]]:
            new2.append(x)
        for x in sorts[2 * i][corssindex[i]:]:
            new2.append(x)
        new_sorts.append(new1)
        new_sorts.append(new2)
    if len(sorts) % 2 == 1:  # 个体数为奇数个，将父代最后一个保留到子代中
        new_sorts.append(sorts[len(sorts) - 1])

    # 变异
    Mutation = np.random.uniform(0.001, 0.04)  # 在0.01~0.2之间随机产生一个数作为变异率
    Mutation_num = int(np.floor(Mutation * Len))  # 变异的数目
    Mutations = np.random.randint(0, len(new_sorts), Mutation_num)  # 随机产生变异的个体编号
    Mutationindex = np.random.randint(0, n, Mutation_num)  # 随机产生变异的个体的变异位置
    s = np.random.randint(0, n, Mutation_num)  # 随机产生突变成的数字
    for i in range(Mutation_num):
        new_sorts[Mutations[i]][Mutationindex[i]] = s[i]
    discard(new_sorts)


def main():
    global n
    global deepth
    deepth=[]
    n = eval(input('请输入皇后个数：'))

    sorts = []
    sorts_size = (np.random.randint(7 * n, 13 * n, size=1))  # 初始化种群的大小
    for i in range(sorts_size[0]):
        sort = np.random.randint(0, n, size=n)
        sorts.append(list(sort))
    for i in range(sorts_size[0]):
        f.write(str(sorts[i]) + '\n')

    sorts = discard(sorts)

    # print(sorts)
    f.write("最后的种群为：" + '\n')
    for i in range(sorts_size[0]):
        f.write(str(sorts[i]) + '\n')
    f.close()


if __name__ == '__main__':
    main()
