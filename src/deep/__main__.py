from deap import base
from deap import creator
from deap import tools
from deap import algorithms
from deep import NQueensProblem

import random
import array

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 16皇后
NUM_OF_QUEENS = 16
# 种群中个体数量
POPULATION_SIZE = 300
# 最大代际数
MAX_GENERATIONS = 100
# 交叉概率
P_CROSSOVER = 0.9
# 　突变概率
P_MUTATION = 0.1

# 使用要解决的问题的大小创建NQueensProblem类的实例
nQueens = NQueensProblem(NUM_OF_QUEENS)
# 由于目标是最大程度地减少违规次数（期望值为0），因此定义最小化适用度策略
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# 定义个体类
creator.create("Individual", array.array, typecode='i', fitness=creator.FitnessMin)
# 由于解由有序的整数列表表示，每个整数表示皇后的列位置，因此使用以下定义来创建初始种群
toolbox = base.Toolbox()
toolbox.register("randomOrder", random.sample, range(len(nQueens)), len(nQueens))

toolbox.register("individualCreator", tools.initIterate, creator.Individual, toolbox.randomOrder)
toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)


# 设置适应度函数以计算皇后在棋盘上的放置所引起的违规次数
def getViolationCount(individual):
    return nQueens.getViolationsCount(individual),


toolbox.register("evaluate", getViolationCount)
# 定义遗传算子
toolbox.register("select", tools.selTournament, tournsize=2)
toolbox.register("mate", tools.cxUniformPartialyMatched, indpb=2.0 / len(nQueens))
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=1.0 / len(nQueens))

# 名人堂成员数量
HALL_OF_FAME_SIZE = 30


def eaSimpleWithElitism(population,
                        toolbox,
                        cxpb,
                        mutpb,
                        ngen,
                        stats=None,
                        halloffame=None,
                        verbose=__debug__):
    """使用halloffame来实现精英机制。 包含在名人堂麦中的个体被直接注入下一代，并且不受选择，交叉和突变的遗传算子的影响。
    """

    logbook = tools.Logbook()  # 用于监控算法运行，和统计数据
    logbook.header = ['gen', 'nevals'] + (stats.fields if stats else [])

    # 计算个体适应度
    invalid_ind = [ind for ind in population if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    if halloffame is None:
        raise ValueError("halloffame parameter must not be empty!")
    # 更新名人堂成员
    halloffame.update(population)
    hof_size = len(halloffame.items) if halloffame.items else 0

    record = stats.compile(population) if stats else {}
    logbook.record(gen=0, nevals=len(invalid_ind), **record)
    if verbose:
        print(logbook.stream)

    # 开始遗传流程
    for gen in range(1, ngen + 1):
        # 选择个体数目=种群个体数-名人堂成员数
        offspring = toolbox.select(population, len(population) - hof_size)

        # 种群更新到下一代
        offspring = algorithms.varAnd(offspring, toolbox, cxpb, mutpb)

        # 计算个体适应度
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # 将名人堂成员添加到当前代
        offspring.extend(halloffame.items)

        # 更新名人堂
        halloffame.update(offspring)

        # 使用当前代替换种群
        population[:] = offspring

        # 将当前统计信息附加到日志
        record = stats.compile(population) if stats else {}
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)
        if verbose:
            print(logbook.stream)

    return population, logbook


def main():
    # 创建初始种群
    population = toolbox.populationCreator(n=POPULATION_SIZE)

    # 注册要监听的统计对象
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("min", np.min)
    stats.register("avg", np.mean)

    # 实例化名人堂对象
    hof = tools.HallOfFame(HALL_OF_FAME_SIZE)

    # 运行遗传算法
    population, logbook = eaSimpleWithElitism(population,
                                              toolbox,
                                              cxpb=P_CROSSOVER,
                                              mutpb=P_MUTATION,
                                              ngen=MAX_GENERATIONS,
                                              stats=stats,
                                              halloffame=hof,
                                              verbose=True)

    # 打印名人堂成员
    print("- Best solutions are:")
    for i in range(HALL_OF_FAME_SIZE):
        print(i, ": ", hof.items[i].fitness.values[0], " -> ", hof.items[i])

    # 绘制统计结果
    minFitnessValues, meanFitnessValues = logbook.select("min", "avg")
    plt.figure(1)
    sns.set_style("whitegrid")
    plt.plot(minFitnessValues, color='red')
    plt.plot(meanFitnessValues, color='green')
    plt.xlabel('Generation')
    plt.ylabel('Min / Average Fitness')
    plt.title('Min and Average fitness over Generations')

    # 绘制最佳解
    sns.set_style("whitegrid", {'axes.grid': False})
    nQueens.plotBoard(hof.items[0])

    # 绘制结果显示
    plt.show()


if __name__ == "__main__":
    main()