import random
import copy
import math

def initSample(size):
    ans = [0 for _ in range(size)]
    for row in range(size):
        col = random.randint(0, size - 1)
        ans[row] = col
    return ans


def numOfConflict(sample):
    size = len(sample)
    conflicts = 0
    for i in range(size):
        for j in range(i+1, size):
            if sample[i] == sample[j] or (j-i) == abs(sample[i]-sample[j]):
                conflicts += 1
    return conflicts

def simulatedAnnealing(sample, temperature):
    size = len(sample)
    for i in range(size):
        curr = numOfConflict(sample)
        if curr == 0:
            return True, sample
        j = random.randint(0, size - 1)
        if sample[i] == j:
            continue
        tmp = copy.deepcopy(sample)
        tmp[i] = j
        attempt = numOfConflict(tmp)
        if attempt <= curr:
            sample = copy.deepcopy(tmp)
        else:
            prob = math.exp( (curr - attempt) / temperature )
            if prob > random.random():
                sample = copy.deepcopy(tmp)
    return False, sample


def display(sample):
    size = len(sample)
    map = [[0 for _ in range(size)] for _ in range(size)]
    for i in range(size):
        map[i][ sample[i] ] = 1
        print(map[i])


# option = "simulate_annealing"
if __name__ == '__main__':
    size = 10
    temperature = 500
    rate = 0.95
    epoch = 0

    ans = initSample(size)
    while True:
        epoch += 1
        flag, ans = simulatedAnnealing(ans, temperature)
        if flag:
            print("Success, ", epoch)
            display(ans)
            break
        temperature *= rate
