import numpy as np
import random



def attacked_queens_pairs(seqs):
    """
    计算序列对应棋盘的【互相攻击的皇后对数n】
    只需要检查当前棋盘的八个皇后在各自的行和两条对角线上是否有其他皇后，不需判断同列是否有其他皇后
    """
    a = np.array([0] * 81)  # 创建一个有81个0的一维数组
    a = a.reshape(9, 9)  # 改为9*9二维数组。为方便后面使用，只用后八行和后八列的8*8部分，作为一个空白棋盘
    n = 0  # 互相攻击的皇后对数初始化为0

    for i in range(1, 9):
        if seqs[i-1] != 0: # seqs的某一元素为0代表对应棋盘的该列不应该放置任何皇后
            a[seqs[i - 1]][i] = 1  # 根据序列，按从第一列到最后一列的顺序，在空白棋盘对应位置放一个皇后，生成当前序列对应的棋盘

    for i in range(1, 9):
        if seqs[i - 1] == 0:
            continue # seqs的某一元素为0代表着对应的棋盘该列未放置任何皇后，直接进行下一列的判断
        for k in list(range(1, i)) + list(range(i + 1, 8 + 1)):  # 检查每个皇后各自所在的行上是否有其他皇后
            if a[seqs[i - 1]][k] == 1:  # 有其他皇后
                n += 1
        t1 = t2 = seqs[i - 1]
        for j in range(i - 1, 0, -1):  # 看左半段的两条对角线
            if t1 != 1:
                t1 -= 1
                if a[t1][j] == 1:
                    n += 1  # 正对角线左半段上还有其他皇后

            if t2 != 8:
                t2 += 1
                if a[t2][j] == 1:
                    n += 1  # 次对角线左半段上还有其他皇后

        t1 = t2 = seqs[i - 1]
        for j in range(i + 1, 8 + 1):  # 看右半段的两条对角线
            if t1 != 1:
                t1 -= 1
                if a[t1][j] == 1:
                    n += 1  # 正对角线右半段上还有其他皇后

            if t2 != 8:
                t2 += 1
                if a[t2][j] == 1:
                    n += 1  # 次对角线右半段上还有其他皇后
    return int(n/2)  # 返回n/2，因为A攻击B也意味着B攻击A，因此返回n的一半


def display_board(seqs):
    """
     显示序列对应的棋盘
    """
    board = np.array([0] * 81)  # 创建一个有81个0的一维数组
    board = board.reshape(9, 9)  # 改变为9*9二维数组，为了后面方便使用，只用后八行和后八列的8*8部分，作为一个空白棋盘

    for i in range(1, 9):
        board[seqs[i - 1]][i] = 1  # 根据序列，从第一列到最后一列的顺序，在对应位置放一个皇后，生成当前序列对应的棋盘
    print('对应棋盘如下:')
    for i in board[1:]:
        for j in i[1:]:
            print(j, ' ', end="")  # 有了end=""，print就不会换行
        print()  # 输出完一行后再换行，这里不能是print('\n')，否则会换两行
    print('攻击的皇后对数为' + str(attacked_queens_pairs(seqs)))



frontier_priority_queue = [{'unplaced_queens': 8, 'pairs':28, 'seqs': [0] * 8}]
# 初始状态为8个0，代表棋盘上无皇后；g(n)=未放置好的皇后个数，h(n)=互相攻击的皇后对数，初始设h(n)=28，g(n)=8
solution = []
flag = 0 # 代表还未找到解


while frontier_priority_queue: # 若frontier非空就继续循环，若成功找到解则跳出循环输出解，若frontier为空时还未找到解则宣告失败
    first = frontier_priority_queue.pop(0)  # 由于每次都会将frontier排序，所以扩展的是第一个序列
    if first['pairs'] == 0 and first['unplaced_queens'] == 0: # 扩展节点前做goal test：若序列h(n)=g(n)=0，则序列为解序列
        solution = first['seqs']
        flag = 1  # 成功
        break
    nums = list(range(1, 9))  # 元素为1-8
    seqs = first['seqs']
    if seqs.count(0) == 0: # 由于后面代码中的排序机制可能将【8个皇后已放好，即g(n)=0，但互相攻击的皇后对数接近于0，但是不为0，即h(n)!=0】的节点放在首位；而此类节点肯定不符合要求，但是这样的节点是无法扩展的，因为8个皇后已经放完了
        continue # 只能跳过这种节点
    for j in range(8): # 在序列中第一个为0的位置，即最左未放置皇后的列中挑选一行放置皇后
        pos = seqs.index(0)
        temp_seqs = list(seqs)
        temp = random.choice(nums)  # 在该列随机挑选一行放置皇后
        temp_seqs[pos] = temp # 将皇后放在该列的第temp行
        nums.remove(temp)  # 从nums移除已产生的值
        frontier_priority_queue.append({'unplaced_queens':temp_seqs.count(0), 'pairs':attacked_queens_pairs(temp_seqs),'seqs':temp_seqs})
    frontier_priority_queue = sorted(frontier_priority_queue, key=lambda x:(x['pairs']+x['unplaced_queens']))

if solution:
    print('已找到解序列：' + str(solution))
    display_board(solution)
else:
    print('算法失败，未找到解')
