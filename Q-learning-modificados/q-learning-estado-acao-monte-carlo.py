import numpy as np
import time

BOARD_ROWS = 5
BOARD_COLS = 5
WIN_STATE = (4, 4)
LOSE_STATE = (4, 0)
REWARD_RATE = 1000

state_values = {}

for i in range(BOARD_COLS):
    for j in range(BOARD_ROWS):
        state_values[(i, j)] = 0

class State:
    def __init__(self, state=(0, 0)):
        self.board = np.zeros([BOARD_ROWS, BOARD_COLS])
        self.state = state
        self.isEnd = False

    def giveReward(self, rewardRate):
        if self.state == WIN_STATE:
            return rewardRate
        elif self.state == LOSE_STATE:
            return -rewardRate
        else:
            return -1

    def isEndFunc(self):
        if (self.state == WIN_STATE) or (self.state == LOSE_STATE):
            self.isEnd = True

    def nxtPosition(self, action):

        if action == "up":
            nxtState = (self.state[0] - 1, self.state[1])
        elif action == "down":
            nxtState = (self.state[0] + 1, self.state[1])
        elif action == "left":
            nxtState = (self.state[0], self.state[1] - 1)
        else:
            nxtState = (self.state[0], self.state[1] + 1)

        if (nxtState[0] >= 0) and (nxtState[0] <= BOARD_COLS - 1):
            if (nxtState[1] >= 0) and (nxtState[1] <= BOARD_ROWS - 1):
                return nxtState
        return self.state

    def nxtPositionDeterministic(self, action, state):
    
        if action == "up":
            nxtState = (state[0] - 1, state[1])
        elif action == "down":
            nxtState = (state[0] + 1, state[1])
        elif action == "left":
            nxtState = (state[0], state[1] - 1)
        else:
            nxtState = (state[0], state[1] + 1)

        if (nxtState[0] >= 0) and (nxtState[0] <= BOARD_COLS - 1):
            if (nxtState[1] >= 0) and (nxtState[1] <= BOARD_ROWS - 1):
                return nxtState
        return -1

class Agent:

    def __init__(self):
        self.episodes = []
        self.actions = ["up", "down", "left", "right"]
        self.State = State()
        self.discountFactor = 0.6

        self.returns = {(i, j):list() for i in range(BOARD_COLS) for j in range(BOARD_ROWS)}

    def chooseAction(self):

        temp = self.actions.copy()

        if self.State.state[0] == 0:
            temp.remove('up')
        if self.State.state[1] == 0:
            temp.remove('left')

        if self.State.state[0] == BOARD_COLS - 1:
            temp.remove('down')
        if self.State.state[1] == BOARD_ROWS - 1:
             temp.remove('right')

        action = np.random.choice(temp)
        
        return action

    def takeAction(self, action):
        position = self.State.nxtPosition(action)
        return State(state=position)

    def reset(self):
        self.episodes = []
        self.State = State()

    def train(self):
        i = 0
        self.State.state = (np.random.randint(0, BOARD_ROWS),np.random.randint(0, BOARD_COLS))
        self.State.isEndFunc()
        #print("State", self.State.state)         
        while True:
            if self.State.isEnd:
                return i
            action = self.chooseAction()
            #print("Action", action)
            reward = self.State.giveReward(REWARD_RATE)
            #print("Reward", reward)
            self.episodes.append([self.State.state, action, reward])
            self.State = self.takeAction(action)
            #print("New State", self.State.state)
            self.State.isEndFunc()
            i += 1
        return i

    def translateCoords(self, state):
        k = 0
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if state == (i, j):
                    return k
                k += 1

    def showValues(self):
        print('----------------------------------')
        for i in range(BOARD_COLS):
            for j in range(BOARD_ROWS):
                print(' | ' + str(state_values[(i, j)]), end = ' | ')
            print(' ')
            print('----------------------------------')


    def chooseActionDeterministc(self):
        mx_nxt_reward = 0
        action = self.actions[0]
        for move in self.actions:
            nextState = self.State.nxtPositionDeterministic(move, self.State.state)
            if nextState != -1:
                action = move
                nxt_reward = state_values[nextState]
                if nxt_reward >= mx_nxt_reward:
                    action = move
                    mx_nxt_reward = nxt_reward

        return action

    def play(self):
        self.State.state = (0, 0)
        while(self.State.state != WIN_STATE):
            action = self.chooseActionDeterministc()
            print("current position {} action {}".format(
                self.State.state, action))
            self.State = self.takeAction(action)
            print("next state ", self.State.state)

        print("End Game")


if __name__ == "__main__":
    roundsAVG = []
    timeAVG = []
    temp = 0
    tempTime = 0

    qntRun = 100000
    for i in range(qntRun):
        last_time = time.time()
        ag = Agent()
        roundTemp = ag.train()
        G = 0
        # print(roundTemp)
        roundsAVG.append(roundTemp)
        #print('Frame took {} seconds'.format(time.time()-last_time))
        timeAVG.append(time.time()-last_time)
        #print("Episodes Main: ", ag.episodes)

        for episode in reversed(ag.episodes):
            #print("Episode: ", episode)
            ag.episodes.pop()
            G = ag.discountFactor * G + episode[2]
            #print("G: ", G)
            #print("Episode[0]", episode)
            #print("index: ", ag.episodes.index(episode))
            #print("List of States: ", list_of_states)
            if episode[0] not in ag.episodes:
                ag.returns[episode[0]].append(G)
                new_value = np.average(ag.returns[episode[0]])
                state_values[(episode[0][0], episode[0][1])] = round(new_value, 3)
                #print(ag.state_values)
        

    for i in range(len(roundsAVG)):
        temp += roundsAVG[i]
        tempTime += timeAVG[i]

    roundsAVG = temp/qntRun
    timeAVG = tempTime/qntRun

    print('Average rounds needed to converg: ', roundsAVG)
    print('Average time needed to converg: ', timeAVG)
    ag.showValues()
    #ag.play()
