from interpreter import interpreter

interpreter.llm.model = "gpt-4o-mini"
response = interpreter.chat("Testing testing 1 2 3", display=False)

print("response:", response)


