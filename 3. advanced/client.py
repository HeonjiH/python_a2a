from python_a2a import A2AClient

#Create a client
client = A2AClient('http://localhost:5000')

#Print agent information
print(f"Connected to: {client.agent_card.name}")
print(f"Description: {client.agent_card.description}")
print(f"Skills: {[skill.name for skill in client.agent_card.skills]}")

#Send a greeting
request = 'Hello!'
print(request)
response = client.ask(request)
print(f"Response: {response}")

#Send another message
request2 = "What's the weather in Paris?"
response = client.ask(request2)
print(request2)
print(f"Response: {response}")

#Send another message
request3 = "Suggest cool places with museums"
response = client.ask(request3)
print(request3)
print(f"Response: {response}")