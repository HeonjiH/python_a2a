# ui_agent.py
from python_a2a import A2AServer, skill, agent, run_server, A2AClient
from python_a2a import TaskStatus, TaskState

@agent(
    name="Travel Assistant",
    description="Your personal travel assistant",
    version="1.0.0"
)
class AssistantAgent(A2AServer):

    def __init__(self):
        super().__init__()
        # Connect to other agents
        self.weather_client = A2AClient("http://localhost:5001")
        self.travel_client = A2AClient("http://localhost:5002")

    def handle_task(self, task):
        # Extract message text
        message_data = task.message or {}
        content = message_data.get("content", {})
        text = content.get("text", "") if isinstance(content, dict) else ""

        # Initialize response
        response_text = "I'm your travel assistant. I can help with weather information and travel recommendations."

        # Determine which agent to route to
        if "weather" in text.lower() or "forecast" in text.lower() or "temperature" in text.lower():
            # Route to weather agent
            response_text = self.weather_client.ask(text)
        elif "recommend" in text.lower() or "suggest" in text.lower() or "destination" in text.lower() or "where should" in text.lower():
            # Route to travel agent
            response_text = self.travel_client.ask(text)
        elif text.lower() in ["hi", "hello", "hey"]:
            # Greeting
            response_text = "Hello! I'm your travel assistant. I can help with weather information and travel recommendations. Try asking about the weather in a city or for recommendations for warm places with beaches."
        elif "help" in text.lower() or "what can you do" in text.lower():
            # Help message
            response_text = """I can help you with:

            1. Weather information: "What's the weather in Paris?" or "Get me the forecast for Tokyo"
            2. Travel recommendations: "Recommend warm destinations" or "Suggest cool places with museums"

            Just let me know what you're interested in!"""

        # Create response artifact
        task.artifacts = [{
            "parts": [{"type": "text", "text": response_text}]
        }]
        task.status = TaskStatus(state=TaskState.COMPLETED)

        return task

# Run the server
if __name__ == "__main__":
    agent = AssistantAgent()
    run_server(agent, port=5000)