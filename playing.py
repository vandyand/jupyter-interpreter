#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# get_ipython().system('pip install open-interpreter')


# In[ ]:


from interpreter import OpenInterpreter
import openai


# In[ ]:


def print_agent_attrs(agent):
    # Get the dictionary of attributes
    attributes = agent.__dict__
    
    # Create a list of tuples containing key and type of value
    attributes_with_types = [(key, type(value).__name__) for key, value in attributes.items()]
    
    # Print the result
    for key, value_type in attributes_with_types:
        print(f"{key}: {value_type}")


# In[ ]:


def util_read_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    return content

def get_prompt(name):
    filepath = f"prompts/{name}.txt"
    return util_read_file(filepath)

def get_current_task():
    return util_read_file("current_task.txt")


# In[ ]:


import time

class FIFOQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, items):
        timestamp = time.time()
        if not isinstance(items, list):
            items = [items]
        self.queue.append({"timestamp": timestamp, "messages": items})

    def dequeue(self):
        if not self.is_empty():
            return self.queue.pop(0)
        else:
            raise IndexError("Dequeue from an empty queue")

    def is_empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)


# In[82]:


import openai
from openai import OpenAI
import os
import time

def save_and_print(message, log_file='agent_log.txt'):
    timestamp = int(time.time())
    message_with_timestamp = f"[{timestamp}] {message}"
    print(message_with_timestamp)
    with open(log_file, 'a') as f:
        f.write(message_with_timestamp + '\n')

class Agent:
    def __init__(self, name, special_commands="", mode="OpenInterpreter", context_window=128000, max_tokens=10000):
        self.name = name
        self.states = ["SPECTATE", "MUTATE", "DICTATE"]
        self.state = "SPECTATE"
        self.inbox = FIFOQueue()
        self.internal_state = []
        self.mode = mode
        self.model = "gpt-4o-mini"
        self.context_window = context_window
        self.max_tokens = max_tokens
        self.generated_new_messages = []
        self.most_recently_received_messages = []
        self.other_agents = []

        if self.mode == "OpenInterpreter":
            self.oi = OpenInterpreter()
            self.oi.llm.model = self.model
            self.oi.llm.context_window = self.context_window
            self.oi.llm.max_tokens = self.max_tokens
            self.oi.system_message += special_commands
            self.system_message = self.oi.system_message
            self.oi.auto_run = True
            self.oi.loop = False
        elif self.mode == "OpenAI":
            self.system_message = special_commands

    def add_other_agent(self, agent):
        self.other_agents.append(agent)

    def handle_state(self):
        save_and_print(f"[{self.name}] Current State: {self.state}")

        if self.state == "SPECTATE":
            if not self.inbox.is_empty():
                self.most_recently_received_messages = self.inbox.dequeue()["messages"]
                save_and_print(f"[{self.name}] Received message(s)")
                self.state = "MUTATE"

        elif self.state == "MUTATE":
            self.internal_state.extend(self.swap_roles(self.most_recently_received_messages))
            save_and_print(f"[{self.name}] Internal state mutated")
            if self.mode == "OpenInterpreter":
                self.generated_new_messages = self.oi.chat(self.internal_state, display=True, stream=False, blocking=True)
            elif self.mode == "OpenAI":
                self.generated_new_messages = self.openai_chat(self.internal_state)
            elif self.mode == "Human":
                self.generated_new_messages = [{"role":"user", "content": self.blocking_input("Enter message:"), "type": "message"}]
            save_and_print(f"[{self.name}] Generated new message(s)")
            if self.mode == "OpenAI":
                save_and_print(f"[{self.name}] New message(s): {self.generated_new_messages}")
            self.state = "DICTATE"

        elif self.state == "DICTATE":
            self.send_message_to_agents(self.generated_new_messages)
            self.generated_new_messages = []
            self.most_recently_received_messages = []
            self.state = "SPECTATE"

        save_and_print(f"[{self.name}] New State: {self.state}")

    def send_message_to_agents(self, messages):
        for agent in self.other_agents:
            agent.inbox.enqueue(messages)
            save_and_print(f"[{self.name}] Sent message to {agent.name}")

    def swap_roles(self, messages):
        for message in messages:
            if message['role'] == 'user':
                message['role'] = 'assistant'
            elif message['role'] == 'assistant':
                message['role'] = 'user'
        return messages

    def blocking_input(self, prompt):
        print(prompt, end='', flush=True)
        while True:
            response = input()
            if response:
                return response
            time.sleep(0.1)

    def openai_chat(self, messages):
        if self.mode != "OpenAI":
            return None

        for message in messages:
            if message["role"] not in ["system", "user", "assistant"]:
                message["role"] = "assistant"
        
        response_content = OpenAI().chat.completions.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[
                {
                    "role":"system",
                    "content": self.system_message
                },
                *messages
            ],
        ).choices[0].message.content
        return [{"role":"assistant", "content": response_content, "type": "message"}]



# In[ ]:


# Read Agent Prompts from prompts directory                                                                     
roadmapper_prompt = """                                                                                         
You are the Roadmap Architect, responsible for creating a structured project roadmap based on the provided      
requirements. Your tasks include identifying tasks, milestones, and their dependencies.                         
To create the roadmap.json file, follow these steps:                                                            
                                                                                                               
1. Review unstructured project documents to identify key tasks and milestones.                                  
2. Create detailed and clear descriptions for each task, ensuring all necessary information is included.        
3. Initially, each task should have "NOT_STARTED" status.                                                       
4. Ensure each task has a unique, auto-incrementing ID starting with 1.                                         
5. Save the structured tasks into the "roadmap.json" file. Create this file if it doesn't exist.   

tasks in roadmap should be of form:
{                                                                                                               
   "id": string of form 'int' or 'int.int' or 'int.int.int...' (auto-incrementing, example: '9.2.3' would be third subtask under second subtask under task '9'),
   "depends_on": list[string<id>] (ids of tasks this one depends on),                                                 
   "type": "TASK" | "MILESTONE",                                                                               
   "name": string (task name),                                                                                 
   "description": string (task details),                                                                       
   "completion_criteria": string (what needs to be accomplished to complete the task),                         
   "status": "NOT_STARTED" | "IN_PROGRESS" | "COMPLETED",                                                      
   "sub_tasks": list[Task] (recursive list of sub-tasks)                                                       
}  
                                                                                                               
Your goal is to provide a clear and organized project roadmap that the project manager and development team c   
follow.                                                                                                         
Outside of these roles, you do not execute any code. You simply organize and structure project information to   
ensure successful project completion.                                                                           
"""                                                                                                             
                                                                                                               
manager_prompt = """                                                                                            
You are the project manager of a dynamic software development team. The current project roadmap is found in t   
file "roadmap.json".                                                                                            
                                                                                                               
Your primary role is to create detailed and clear instructions for developers to follow. Your secondary role    
to update the 'roadmap.json' file by marking tasks as "status": "COMPLETED" when they are done.                 
                                                                                                               
To improve tracking task progress and prevent duplication of effort, follow these steps:                        
1. Instruct the developer to complete the following:                                                            
  a. Make sure the task is working as expected.                                                                
  b. Create a new git branch.                                                                                  
  c. Commit changes to the new git branch.                                                                     
  d. Push the new branch to origin.                                                                            
  e. Update the task status to "status": "COMPLETED" in the 'roadmap.json' file.                               
                                                                                                               
2. Before considering a task complete, verify:                                                                  
  a. The task status in 'roadmap.json' is marked as "status": "COMPLETED".                                     
  b. The changes have been pushed to the origin in the new branch.                                             
  c. If the task is not updated or missing from 'roadmap.json', request the developer to update it             
immediately.                                                                                                    
                                                                                                               
3. If a task status is updated as "status": "COMPLETED" but still appears incomplete, communicate with the      
developer to resolve discrepancies.                                                                             
                                                                                                               
The structure of each task in 'roadmap.json' is as follows:                                                     
{                                                                                                               
   "id": string of form 'int' or 'int.int' or 'int.int.int...' (auto-incrementing, example: '9.2.3' would be third subtask under second subtask under task '9'),
   "depends_on": list[int] (ids of tasks this one depends on),                                                 
   "type": "TASK" | "MILESTONE",                                                                               
   "name": string (task name),                                                                                 
   "description": string (task details),                                                                       
   "completion_criteria": string (what needs to be accomplished to complete the task),                         
   "status": "NOT_STARTED" | "IN_PROGRESS" | "COMPLETED",                                                      
   "sub_tasks": list[Task] (recursive list of sub-tasks)                                                       
}                                                                                                               
                                                                                                               
Outside of these roles, you do not execute any code. You simply provide guidance and direction to the team to   
ensure successful project completion. If the current task has already been completed, please move to the next   
task. If all tasks have been completed please respond with **ALL TASKS COMPLETED -- NOTHING TO DO**.            
"""

dev_prompt = """
You are a key member of a dynamic software development team.

Your primary role is to write, test, and debug code based on the detailed instructions provided by the project manager.

You actively collaborate with other team members to ensure the successful development and implementation of software projects.

Please make sure to run any on-going perpetual services in the background so as not to hang your process.

"""
                                                                                                               
# New Verifier Agent Prompt                                                                                     
verifier_prompt = """                                                                                           
You are the Task Verifier, responsible for ensuring that tasks marked as complete meet all defined completion   
criteria and dependencies.                                                                                      
To perform your role, follow these guidelines:                                                                  
                                                                                                               
1. Before marking any task as "COMPLETED", review the "completion_criteria" defined in the task.                
2. Confirm that:                                                                                                
  a. All dependent tasks are marked as "COMPLETED".                                                            
  b. The developer has provided evidence that the task meets the requirements (e.g., output, results).         
                                                                                                               
3. If the task does not meet the criteria, return feedback to the project manager to address any discrepancie   
or issues with the task completion.                                                                             
                                                                                                               
Your goal is to maintain the integrity of the project roadmap and ensure that no tasks are falsely marked as    
complete.                                                                                                       
"""                                                                                                             
                                                                                                               
# Storing these prompts in a structured way for easy access                                                     
prompts = {                                                                                                     
"roadmapper": roadmapper_prompt,                                                                            
"manager": manager_prompt,
"dev": dev_prompt,
"verifier": verifier_prompt                                                                                 
}  


# In[ ]:


# roadmapper = Agent("Roadmap Architect", prompts["roadmapper"])
pm = Agent("Project Manager", prompts["manager"], mode="OpenAI")
dev = Agent("Software Developer", prompts["dev"])
verifier = Agent("Task verifier", prompts["verifier"], mode="OpenAI")
human = Agent("Human guy", "You are a human", mode="Human")

# roadmapper.add_other_agent(pm)
pm.add_other_agent(dev)
dev.add_other_agent(verifier)
verifier.add_other_agent(human)
human.add_other_agent(pm)

# roadmapper.inbox.enqueue(
#     [{"role": "user", "content": f"Here is the content of the project_description.txt file: \n\n {util_read_file("project_description.txt")}", "type": "message"},
#     {"role": "user", "content": "Please proceed to create a very detailed roadmap.json file complete with nested heirarchical tasks and sub tasks. Please keep creating sub tasks of sub tasks until the deepest sub-tasks are optimally atomic such as to be achievable by an llm-backed open-interpreter ai agent.", "type": "message"}])

pm.inbox.enqueue(
    [{"role": "user", "content": f"Here is the content of the project_description.txt file: \n\n {util_read_file("project_description.txt")}", "type": "message"},
     {"role": "user", "content": f"Here is the content of the roadmap.json file: \n\n {util_read_file("roadmap.json")}", "type": "message"},
    {"role": "user", "content": "Please proceed to instruct the developer on next steps.", "type": "message"}])


while True:
    # roadmapper.handle_state()
    pm.handle_state()
    dev.handle_state()
    verifier.handle_state()
    human.handle_state()





