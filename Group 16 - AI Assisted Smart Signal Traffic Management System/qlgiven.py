import os
import sys
import traci
import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import webbrowser
import tempfile
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Ensure SUMO_HOME is set correctly
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'.")

sumoBinary = "sumo-gui"  # Change to "sumo" for non-GUI version
sumoCmd = [sumoBinary, "-c", "/Users/colinmichael/Desktop/mv/yourNetwork.sumocfg"]

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.gamma = 0.95
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(24, input_dim=self.state_size, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=self.learning_rate))
        return model

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def train(self, state, action, reward, next_state, done):
        target = reward if done else reward + self.gamma * np.amax(self.model.predict(next_state)[0])
        target_f = self.model.predict(state)
        target_f[0][action] = target
        self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

class SumoEnvironment:
    def __init__(self):
        self.agent = DQNAgent(state_size=4, action_size=4)  # Adjust sizes as needed
        self.state = None
        self.waiting_times = []
        self.total_vehicles = 0  # Track the total number of vehicles simulated

    def run(self):
        traci.start(sumoCmd)
        done = False
        total_reward = 0

        while not done:
            traci.simulationStep()
            self.state = self.get_state()
            action = self.agent.act(self.state)
            next_state, reward, done = self.step(action)
            self.agent.train(self.state, action, reward, next_state, done)
            total_reward += reward
            self.track_waiting_time()
            self.total_vehicles += len(traci.vehicle.getIDList())  # Update total vehicles
            
            # Check if the number of vehicles is zero and set done to True if so
            if len(traci.vehicle.getIDList()) == 0:
                done = True

        traci.close()
        print("Total reward:", total_reward)
        print("Total vehicles simulated:", self.total_vehicles)  # Print total vehicles simulated
        self.plot_waiting_time()

    def get_state(self):
        # Implement state extraction from simulation
        return np.random.rand(1, 4)  # Placeholder

    def step(self, action):
        # Implement simulation step forward
        return np.random.rand(1, 4), random.randint(-1, 1), False  # Placeholder

    def track_waiting_time(self):
        vehicles = traci.vehicle.getIDList()
        total_waiting_time = 0
        for vehicle_id in vehicles:
            total_waiting_time += traci.vehicle.getAccumulatedWaitingTime(vehicle_id)
        
        average_waiting_time = total_waiting_time / len(vehicles) if vehicles else 0
        self.waiting_times.append(average_waiting_time)

    def plot_waiting_time(self):
        sns.set(style="whitegrid")  # Set style to white grid
        plt.figure(figsize=(10, 6))
        plt.plot(range(len(self.waiting_times)), self.waiting_times, marker='o', linestyle='-', label='Average Waiting Time', color='b')
        plt.title('Average Waiting Time per Time Step', fontsize=16)
        plt.xlabel('Time Step', fontsize=14)
        plt.ylabel('Average Waiting Time (s)', fontsize=14)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=12)
        plt.legend(fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.show()
        
        # Save the plot as a PNG file and immediately open it in a new browser tab
        temp_file = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
        plt.savefig(temp_file.name)
        plt.close()
        webbrowser.open('file://' + temp_file.name, new=2)  # new=2 opens in a new tab, if possible

if __name__ == "__main__":
    env = SumoEnvironment()
    env.run()
