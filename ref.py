from interpreter import OpenInterpreter

# Create two instances of the interpreter
agent_1 = OpenInterpreter()
agent_1.system_message = "This is a separate instance."

agent_2 = OpenInterpreter()
agent_2.system_message = "This is yet another instance."

# Function to swap roles in messages
def swap_roles(messages):
    for message in messages:
        if message['role'] == 'user':
            message['role'] = 'assistant'
        elif message['role'] == 'assistant':
            message['role'] = 'user'
    return messages

# List of agents
agents = [agent_1, agent_2]

# Initial message
messages = [{"role": "user", "content": "Hello!"}]

# Conversation loop
while True:
    for agent in agents:
        messages = agent.chat(messages)
        messages = swap_roles(messages)
        print(messages)
