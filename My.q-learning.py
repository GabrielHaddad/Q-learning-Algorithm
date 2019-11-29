import numpy as np
import time

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

    def giveReward(self, rewardRate):
        if self.state == WIN_STATE:
            return rewardRate
        elif self.state == LOSE_STATE:
            return -rewardRate
        else:
            return 0

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

class Agent:

    def __init__(self):
        self.states = []
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
        self.states = []
        self.State = State()

    def train(self, rounds=10):
        i = 0
        while i < rounds:
            if self.State.isEnd:
                reward = self.State.giveReward(REWARD_RATE)
                finalState = self.states[-1]
                self.state_values[(self.translateCoords(finalState[0]), self.actions.index(finalState[1]))]
                print("Game End Reward", reward)
                for s in reversed(self.states):
                    reward = self.state_values[(self.translateCoords(s[0]), self.actions.index(s[1]))] + \
                        self.learningRate * (reward + self.discountFactor * self.maxNextPosition(s[0], s[1])) - \
                            self.state_values[(self.translateCoords(s[0]), self.actions.index(s[1]))]
                    self.state_values[(self.translateCoords(s[0]), self.actions.index(s[1]))]  = round(reward, 3)
                self.reset()
                i += 1
            else:
                action = self.chooseAction()
                self.states.append((self.State.state, action))
                print("current position {} action {}".format(
                    self.State.state, action))
                self.State = self.takeAction(action)
                self.State.isEndFunc()
                print("nxt state", self.State.state)
                print("---------------------")

    def maxNextPosition(self, currentState, action):
        mx_nxt_reward = 0
        position = self.State.nxtPosition(currentState)
        for move in self.actions:
            nxt_reward = self.state_values[(self.translateCoords(position), self.actions.index(move))]
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
            print(str([i]), end = ' ') 
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
    ag.train(10000)
    print('Frame took {} seconds'.format(time.time()-last_time))
    ag.showValues()
    ag.play()
