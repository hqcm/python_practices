import Team
import numpy as np
import random


#欧冠小组赛出线需要的最少分数
class Group(object):
    def __init__(self):
        self.data = np.zeros((4, 4), dtype=int)

    def vs(self, a, b):
        self.data[a.level - 1, b.level -
                  1] = random.randint(0, a.level) * 10 + random.randint(
                      0, b.level)

    def compare(self, i, j, a, b):
        if a.score > b.score:
            #1.比较总积分
            return 1
        elif a.score < b.score:
            return 0
        else:
            if (self.data[i - 1, j - 1] + self.data[j - 1, 1 - 1]) >= 4:
                #2.比较相互积分
                return 1
            elif (self.data[i - 1, j - 1] + self.data[j - 1, 1 - 1]) <= 1:
                return 0
            else:
                if self.data[i - 1, j - 1] < 10:
                    home1 = 0
                    away1 = self.data[i - 1, j - 1]
                else:
                    home1 = self.data[i - 1, j - 1] // 10
                    away1 = self.data[i - 1, j - 1] % 10
                if self.data[j - 1, i - 1] < 10:
                    home2 = 0
                    away2 = self.data[j - 1, i - 1]
                else:
                    home2 = self.data[j - 1, i - 1] // 10
                    away2 = self.data[j - 1, i - 1] % 10
                if home1 + away2 - home2 - away1 > 0:
                    #3.比较相互净胜球
                    return 1
                elif home1 + away2 - home2 - away1 > 0:
                    return 0
                else:
                    if away2 > away1:
                        #比较相互客场进球
                        return 1
                    elif away2 < away1:
                        return 0
                    else:
                        if a.netgoal > b.netgoal:
                            #比较小组赛净胜球
                            return 1
                        elif a.netgoal < b.netgoal:
                            return 0
                        else:
                            if a.goal > b.goal:
                                #比较小组赛净胜球
                                return 1
                            elif a.goal < b.goal:
                                return 0
                            else:
                                return random.randint(0, 1)


if __name__ == '__main__':
    k = 100000
    #极限出线情形需要更加大量的样本
    point = []
    while k:
        group = Group()
        team1 = Team.Team()
        team2 = Team.Team()
        team3 = Team.Team()
        team4 = Team.Team()
        team1.level = 1
        team2.level = 2
        team3.level = 3
        team4.level = 4
        for i in range(1, 5):
            for j in range(1, 5):
                if i != j:
                    group.vs(eval("team" + str(i)), eval("team" + str(j)))
        for i in range(1, 5):
            #主场
            for j in range(1, 5):
                if group.data[i - 1, j - 1] < 10:
                    a = 0
                    b = group.data[i - 1, j - 1]
                else:
                    a = group.data[i - 1, j - 1] // 10
                    b = group.data[i - 1, j - 1] % 10
                eval("team" + str(i)).goal += a
                eval("team" + str(i)).lose += b
                eval("team" + str(i)).netgoal += a - b
                if i != j:
                    if a > b:
                        eval("team" + str(i)).score += 3
                    elif a == b:
                        eval("team" + str(i)).score += 1
        for i in range(1, 5):
            #客场
            for j in range(1, 5):
                if group.data[j - 1, i - 1] < 10:
                    a = 0
                    b = group.data[j - 1, i - 1]
                else:
                    a = group.data[j - 1, i - 1] // 10
                    b = group.data[j - 1, i - 1] % 10
                eval("team" + str(i)).goal += b
                eval("team" + str(i)).lose += a
                eval("team" + str(i)).netgoal += b - a
                if i != j:
                    if a < b:
                        eval("team" + str(i)).score += 3
                    elif a == b:
                        eval("team" + str(i)).score += 1
        for i in range(1, 4):
            for j in range(i + 1, 5):
                flag = group.compare(i, j, eval("team" + str(i)),
                                     eval("team" + str(j)))
                if flag:
                    eval("team" + str(i)).rank += 1
                else:
                    eval("team" + str(j)).rank += 1
        for i in range(1, 5):
            if eval("team" + str(i)).rank == 2:
                point.append(eval("team" + str(i)).score)
                break
        k -= 1
    print(min(point))
