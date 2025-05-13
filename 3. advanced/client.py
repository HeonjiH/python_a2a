from python_a2a import A2AClient

#Create a client
client = A2AClient('http://localhost:5000')

#Print agent information
print(f"Connected to: {client.agent_card.name}")
print(f"Description: {client.agent_card.description}")
print(f"Skills: {[skill.name for skill in client.agent_card.skills]}\n")

#Send a greeting
# request = 'Hello!'
# print(f"User: {request}")
# response = client.ask(request)
# print(f"Agent: {response}\n")

# #Send another message
# request2 = "How's the weather in Paris?"
# print(f"User: {request2}")
# response = client.ask(request2)
# print(f"Agent: {response}\n")

#Send another message
request3 = "Suggest mild places with museums"
print(f"User: {request3}")
response = client.ask(request3)
print(f"Agent: {response}\n")