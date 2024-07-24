
# Distributed System Coordination Simulation

import threading
import time

class Agent(threading.Thread):
    def __init__(self, name, task):
        super().__init__()
        self.name = name
        self.task = task

    def run(self):
        print(f'{self.name} started working on {self.task}...')
        time.sleep(2)  # Simulate time taken to complete the task
        print(f'{self.name} has completed {self.task}.')

def main():
    tasks = ['Data Collection', 'Data Processing', 'Data Analysis']
    agents = []

    # Create and start agents
    for i, task in enumerate(tasks):
        agent = Agent(f'Agent-{i + 1}', task)
        agents.append(agent)
        agent.start()

    # Wait for all agents to complete their tasks
    for agent in agents:
        agent.join()

    print('All tasks have been completed!')

if __name__ == '__main__':
    main()
