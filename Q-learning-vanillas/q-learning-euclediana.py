import numpy as np
import time
import math

BOARD_ROWS = 2
BOARD_COLS = 2
WIN_STATE = (1, 1)
LOSE_STATE = (1, 0)
START = (0, 0)
REWARD_RATE = 1000


class State:
    def __init__(self, state=START):
        self.board = np.zeros([BOARD_ROWS, BOARD_COLS])
        self.state = state
        self.isEnd = False

    def rewardFunc(self):
        dist = math.sqrt((self.state[0] - self.state[1])**2 + (WIN_STATE[0] - WIN_STATE[1])**2)

        if self.state == WIN_STATE:
            self.isEnd = True
            return REWARD_RATE
        elif self.state == LOSE_STATE:
            self.isEnd = True
            return -REWARD_RATE
        else:
            return dist

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

class Agent:

    def __init__(self):
        self.actions = ["up", "down", "left", "right"]
        self.State = State()
        self.learningRate = 0.1
        self.greedyValue = 0.9
        self.discountFactor = 0.9

        self.state_values = {}
        for i in range(BOARD_COLS * BOARD_ROWS):
            for j in range(len(self.actions)):
                self.state_values[(i, j)] = 0

    def chooseAction(self):

        mx_nxt_reward = 0
        action = self.actions[0]

        if np.random.uniform(0, 1) <= self.greedyValue:
            action = np.random.choice(self.actions)
        else:
            for move in self.actions:
                nxt_reward = self.state_values[(self.translateCoords(self.State.state), self.actions.index(move))]
                if nxt_reward >= mx_nxt_reward:
                    action = move
                    mx_nxt_reward = nxt_reward
        return action

    def takeAction(self, action):
        position = self.State.nxtPosition(action)
        return State(state=position)

    def reset(self):
        self.State = State()

    def train(self):
        i = 0
        oldTable = self.state_values.copy()
        while True:
            if self.State.isEnd == False:
                oldTable = self.state_values.copy()
                action = self.chooseAction()
                print("current position {} action {}".format(
                    self.State.state, action))
                previousState = self.State.state
                self.State = self.takeAction(action)
                reward = self.State.rewardFunc()
                self.state_values[(self.translateCoords(previousState), self.actions.index(action))] = \
                    round(self.state_values[(self.translateCoords(previousState), self.actions.index(action))] + \
                        self.learningRate * (reward + self.discountFactor * self.maxNextPosition(self.State.state, action) - \
                            self.state_values[(self.translateCoords(previousState), self.actions.index(action))]),3)
                print("nxt state", self.State.state)
                print("---------------------")
            else:
                i += 1
                print(i)
                if oldTable == self.state_values:
                    print(oldTable)
                    print(self.state_values)
                    self.reset()
                    break
                self.reset()
        return i

    def maxNextPosition(self, currentState, action):
        mx_nxt_reward = 0
        for move in self.actions:
            nxt_reward = self.state_values[(self.translateCoords(currentState), self.actions.index(move))]
            if nxt_reward >= mx_nxt_reward:
                mx_nxt_reward = nxt_reward
        
        return mx_nxt_reward

    def translateCoords(self, state):
        k = 0
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                if state == (i, j):
                    return k
                k += 1

    def showValues(self):
        print('----------------------------------')
        for i in range(BOARD_COLS * BOARD_ROWS):
            for j in range(len(self.actions)):
                print(' | ' + str(self.state_values[(i, j)]), end = ' | ')
            print(' ')
            print('----------------------------------')

    def chooseActionDeterministc(self):
        mx_nxt_reward = 0
        action = self.actions[0]
        for move in self.actions:
            nxt_reward = self.state_values[(self.translateCoords(self.State.state), self.actions.index(move))]
            if nxt_reward >= mx_nxt_reward:
                action = move
                mx_nxt_reward = nxt_reward

        return action

    def play(self):
        while(self.State.state != WIN_STATE):
            action = self.chooseActionDeterministc()
            print("current position {} action {}".format(
                    self.State.state, action))
            self.State = self.takeAction(action)
            print("next state ",self.State.state)

        print("End Game")

if __name__ == "__main__":
    ag = Agent()
    last_time = time.time()
    print(ag.train())
    print('Frame took {} seconds'.format(time.time()-last_time))
    ag.showValues()
    # ag.play()

