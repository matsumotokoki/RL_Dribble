import numpy as np
from dribble_env_2d import Dribble_Env
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.utils import plot_model
from collections import deque
from keras import backend as K
import tensorflow  as tf
import time
import math


def huberloss(y_true, y_pred):
    err = y_true - y_pred
    cond = K.abs(err) < 1.0
    L2 = 0.5 * K.square(err)
    L1 = (K.abs(err) - 0.5)
    loss = tf.where(cond,L2,L1)
    return K.mean(loss)

class QNetwork:
    def __init__(self,learning_rate=0.01, state_size=5,action_size=3,hidden_size=10):
        self.action_size = action_size
        self.model = Sequential()
        self.model.add(Dense(hidden_size,activation='relu',input_dim=state_size))
        self.model.add(Dense(hidden_size,activation='relu'))
        self.model.add(Dense(action_size,activation='linear'))
        self.optimizer = Adam(lr=learning_rate)
        self.model.compile(loss=huberloss,optimizer=self.optimizer)

    def replay(self, memory, batch_size, gamma, targetQN):
        inputs = np.zeros((batch_size, 5))
        targets = np.zeros((batch_size, self.action_size))
        mini_batch = memory.sample(batch_size)

        for i, (state_b, action_b, reward_b, next_state_b) in enumerate(mini_batch):
            inputs[i:i+1] = state_b
            target = reward_b

            if not (next_state_b == np.zeros(state_b.shape)).all(axis=1):
                retmainQs = self.model.predict(next_state_b)[0]
                next_action = np.argmax(retmainQs)
                target = reward_b + gamma * targetQN.model.predict(next_state_b)[0][next_action]

            targets[i] = self.model.predict(state_b)
            targets[i][action_b] = target

        self.model.fit(inputs, targets, epochs=1, verbose=0)

class Memory:
    def __init__(self,max_size=1000):
        self.buffer = deque(maxlen=max_size)

    def add(self,experience):
        self.buffer.append(experience)

    def sample(self, batch_size):
        idx = np.random.choice(np.arange(len(self.buffer)),size=batch_size,replace = False)
        return [self.buffer[ii] for ii in idx]

    def len(self):
        return len(self.buffer)

class Actor:
    def get_action(self, state, episode, mainQN):
        epislon = 0.01 + 0.9 /(1.0+episode*0.1)
        if epislon <= np.random.uniform(0,1):
            reTargetQs = mainQN.model.predict(state)[0]
            action = np.argmax(reTargetQs)
        else:
            action = np.random.choice(3)

        return action

METHOD_STR = "DDQN" #DQN or DDQN
RENDER_FLAG = True
num_episodes = 300000
max_number_of_steps = 200
goal_average_reward = 10
num_consecutive_iterations = 10
total_reward_vec = np.zeros(num_consecutive_iterations)
gamma = 0.99
islearnd = False
isrender = False
hidden_size = 16
learning_rate = 0.0001
memory_size = 10000
batch_size = 100
max_step = 0
env = Dribble_Env()


mainQN = QNetwork(hidden_size=hidden_size, learning_rate=learning_rate)
targetQN = QNetwork(hidden_size=hidden_size, learning_rate=learning_rate)
#plot_model(mainQN.model, to_file='Qnetwork.png', show_shapes=True) 
memory = Memory(max_size = memory_size)
actor = Actor()

for episode in range(num_episodes):
    env.reset()
    env.step(np.random.randint(3))
    state = env.get_state()[0:5]
    state = np.reshape(state, [1,5])
    # episode_reward = 0
    targetQN.model.set_weights(mainQN.model.get_weights())

    for t in range(max_number_of_steps):
        if islearnd and RENDER_FLAG:
            env.render()
            time.sleep(0.01)
        env.render()
        time.sleep(0.01)

        action = actor.get_action(state, episode, mainQN)
        env.step((action))
        next_state = env.get_state()[0:5]
        ball_state = env.get_state()[5:7]
        goal_distance = math.sqrt((ball_state[0] + 90)**2 + ball_state[1]**2)
        next_state = np.reshape(next_state,[1,5])
        done = env.check_done()

        if done:
            reward = 10
        elif t == 199:
            # reward = -goal_distance
            reward = -10
        else:
            reward = 0

        # episode_reward += 1
        memory.add((state,action,reward,next_state))
        state = next_state
        
        if (memory.len() > batch_size)  and not islearnd:
            mainQN.replay(memory,batch_size,gamma,targetQN)

        if METHOD_STR=="DQN":
            targetQN.model.set_weights(mainQN.model.get_weights())
        else:
            pass

        if done or t >= 199:
            if max_step < t:
                max_step = t
            total_reward_vec = np.hstack((total_reward_vec[1:], reward))
            ball_state = env.get_state()[5:7]
            # print('{:5d} Episode finished, {:6.2f} steps, ave: {:6.2f}, max: {:4d}'.format(episode,t+1,total_reward_vec.mean(),max_step+1),flush=True)
            print('{:5d} Episode finished, {:7.2f} steps, reward: {:7.2f}, ave: {:7.2f}, ball_x: {:6.2f}, ball_y: {:6.2f}'\
                    .format(episode+1,t+1,reward,total_reward_vec.mean(),ball_state[0],ball_state[1]),flush=True)
            break

    if total_reward_vec.mean() >= goal_average_reward:
        if not islearnd:
            print('Episode {:5d} train agent successfuly!'.format(episode+1))
        islearnd = True
        if not isrender:
            isrender = True
