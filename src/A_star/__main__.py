import numpy as np
import random


def attacked_queens_pairs(seqs):
    a = np.array([0] * (size+1)*(size+1))
    a = a.reshape(size+1, size+1)
    n = 0

    for i in range(1, size+1):
        if seqs[i-1] != 0:
            a[seqs[i-1][i]] = 1

    for i in range(1, size+1):
        if seqs[i-1] == 0:
            continue
        for k in list(range(1, i)) + list(range(i + 1, size + 1)):
            if a[seqs[i-1][k]] == 1:
                n += 1
        t1 = t2 = seqs[i-1]
        for j in range(i - 1, 0, -1):
            if t1 != 1:
                t1 -= 1
                if a[t1][j] == 1:
                    n += 1
        t1 = t2 = seqs[i-1]
        for j in range(i + 1, size + 1):
            if t1 != 1:
                t1 -= 1
                if a[t1][j] == 1:
                    n += 1

            if t2 != 8:
                t2 += 1
                if a[t2][j] == 1:
                    n += 1
    return int(n/2)


def display_board(seqs):
    board = np.array([0] * (size+1)*(size+1))
    board = board.reshape(size+1, size+1)

    for i in range(1, size+1):
        board[seqs[i - 1]][i] = 1
    print('对应棋盘如下:')
    for i in board[1:]:
        for j in i[1:]:
            print(j, ' ', end="")
        print()
    print('攻击的皇后对数为' + str(attacked_queens_pairs(seqs)))


if __name__ == '__main__':
    size = 8
    frontier_priority_queue = [{'unplaced_queens': 8, 'pairs': 28, 'seqs': [0] * size}]
    closed = []
    flag = 0

    while frontier_priority_queue:
        first = frontier_priority_queue.pop(0)
        if first['pairs'] == 0 and first['unplaced_queens'] == 0:
            closed = first['seqs']
            flag = 1
            break
        nums = list(range(1, size + 1))
        seqs = first['seqs']
        if seqs.count(0) == 0:
            continue
        for j in range(size):
            pos = seqs.index(0)
            temp_seqs = list(seqs)
            temp = random.choice(nums)
            nums.remove(temp)
            frontier_priority_queue.append(
                {'unplaced_queens': temp_seqs.count(0), 'pairs': attacked_queens_pairs(temp_seqs), 'seqs': temp_seqs})
        frontier_priority_queue = sorted(frontier_priority_queue, key=lambda x: (x['pairs']+x['unplaced_queens']))

if closed:
    print('find')
else:
    print('error')
