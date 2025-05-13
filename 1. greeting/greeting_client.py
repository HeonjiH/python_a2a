from python_a2a import A2AClient

#Create a client
client = A2AClient('http://localhost:5000')

#Print agent information
print(f"Connected to: {client.agent_card.name}")
print(f"Description: {client.agent_card.description}")
print(f"Skills: {[skill.name for skill in client.agent_card.skills]}")

#Send a greeting
request = 'Hello there! My name is Alice'
print(request)
response = client.ask(request)
print(f"Response: {response}")

#Send another message
response = client.ask("What can you do?")
print("What can you do?")
print(f"Response: {response}")