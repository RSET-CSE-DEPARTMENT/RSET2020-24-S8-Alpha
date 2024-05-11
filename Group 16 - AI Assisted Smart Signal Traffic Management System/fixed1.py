import os
import sys
import traci
import matplotlib.pyplot as plt
import seaborn as sns
import tempfile
import webbrowser
import random
from sumo_rl import SumoEnvironment

# Ensure the SUMO_HOME environment variable is correctly set
if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'.")

def plot_waiting_times(waiting_times, run):
    sns.set(style="darkgrid")
    plt.figure(figsize=(10, 6))
    plt.plot(waiting_times, marker='o', linestyle='-', label='Average Waiting Time')
    plt.title(f'Average Waiting Time per Time Step - Run {run}')
    plt.xlabel('Time Step')
    plt.ylabel('Average Waiting Time (s)')
    plt.legend()
    plt.tight_layout()
    temp_file_png = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    plt.savefig(temp_file_png.name)
    plt.close()
    webbrowser.open(f'file://{temp_file_png.name}', new=2)

# Main simulation logic
if __name__ == "__main__":
    initial_green_duration = 10  # Initial green duration in seconds
    initial_red_duration = 5     # Initial red duration in seconds
    change_interval = 5          # Interval in seconds after which durations change

    # Number of episodes (simulations)
    episodes = 1
    env = SumoEnvironment(
        net_file="yourNetwork.net.xml",
        route_file="yourRoutes.rou.xml",
        use_gui=True,
        num_seconds=80000,
        min_green=5,
        delta_time=5,
    )

    # Loop for each episode
    for episode in range(1, episodes + 1):
        env.reset()  # Reset the environment at the start of each episode
        done = {"__all__": False}
        current_time = 0  # Track the current time to manage signal changes
        green_duration = initial_green_duration
        red_duration = initial_red_duration
        waiting_times = []  # Track waiting times for the current run

        while not done["__all__"]:
            actions = {}
            for ts in env.ts_ids:  # Iterate over all traffic signals
                # Determine the phase based on the current time in the simulation
                # This simple logic alternates between green and red phases based on updated durations
                phase_duration = green_duration if (current_time // (green_duration + red_duration)) % 2 == 0 else red_duration
                actions[ts] = 1 if phase_duration == green_duration else 0  # Assuming 0 is green and 1 is red in your environment's action space
                current_time += 1

            # Check if it's time to change durations
            if current_time % change_interval == 0:
                # Generate new durations randomly
                new_green_duration = random.randint(5, 15)  # Example: Random duration between 5 and 15 seconds
                new_red_duration = random.randint(3, 8)     # Example: Random duration between 3 and 8 seconds

                green_duration = new_green_duration
                red_duration = new_red_duration

            observations, rewards, dones, info = env.step(action=actions)
            current_time += env.delta_time  # Increment current time by the environment's time step
            
            # Track waiting times
            vehicles = traci.vehicle.getIDList()
            total_waiting_time = 0
            for vehicle_id in vehicles:
                total_waiting_time += traci.vehicle.getAccumulatedWaitingTime(vehicle_id)
            
            average_waiting_time = total_waiting_time / len(vehicles) if vehicles else 0
            waiting_times.append(average_waiting_time)

            if len(vehicles) == 0:  # Check if there are no vehicles in the network
                done["__all__"] = True  # End simulation if no vehicles are present

        traci.close()  # Close the simulation for the current episode
        plot_waiting_times(waiting_times, episode)  # Plot waiting times for the current episode