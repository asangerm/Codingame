import sys

class Game:
    def __init__(self, piste, pos, count, unused):
        self.piste = piste
        self.pos = pos
        self.count = count
        self.unused = unused

class Score:
    def __init__(self, score, game1, game2, game3, game4):
        self.score = score
        self.game1 = game1
        self.game2 = game2
        self.game3 = game3
        self.game4 = game4

def is_there_a_hash(piste, pos):
    for i in range(pos, len(piste)):
        if piste[i] == '#':
            return (1)
    return (0)

def gimme_next_hash(game):
    next_hash = []
    for i in game:
        position = 0
        for j in range(len(i.piste)):
            if j >= i.pos[0]:
                if i.piste[j] != '#':
                    position += 1
                else:
                    break
        if is_there_a_hash(i.piste, i.pos[0]) == 0:
            position = 200
        next_hash.append(position)
        print(position, file=sys.stderr)
    return (next_hash)

def get_min(hash):
    mini = 1000
    for i in hash:
        if i < mini and i > 0:
            mini = i
    c = 0
    d = 0
    if mini == 1:
        for i in hash:
            if i == 2:
                c+=1
            #if i >= 4:
                #d+=1
    #if d >= 2:
        #return(4)
    if c >= 2:
        return (2)
    return (mini)

player_id = int(input())
nb_games = int(input())


# game loop
while True:
    games = []
    scores = []
    for i in range(3):
        score_info = input().split()
        point, or1, ar1, br1, or2, ar2, br2, or3, ar3, br3, or4, ar4, br4 = [int(j) for j in score_info]
        scores.append(Score(point, [or1, ar1, br1], [or2, ar2, br2], [or3, ar3, br3], [or4, ar4, br4]))
    
    for i in range(nb_games):
        inputs = input().split()
        gpu = inputs[0]
        reg_0 = int(inputs[1])
        reg_1 = int(inputs[2])
        reg_2 = int(inputs[3])
        reg_3 = int(inputs[4])
        reg_4 = int(inputs[5])
        reg_5 = int(inputs[6])
        reg_6 = int(inputs[7])
        games.append(Game(gpu, [reg_0, reg_1, reg_2], [reg_3, reg_4, reg_5], reg_6))
    
    next_hash = gimme_next_hash(games)
    mini = get_min(next_hash)
    print("mini = ", mini, file=sys.stderr)

    if mini == 1:
        print("UP")
    elif mini == 2:
        print("LEFT")
    elif mini == 3:
        print("UP")
    else:
        print("RIGHT")
