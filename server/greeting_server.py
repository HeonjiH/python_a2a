from python_a2a import A2AServer, skill, agent, run_server
from python_a2a import TaskStatus, TaskState

# Agent Card
@agent(
    name="Greeting Agent",
    description="A simple agent that responds to greetings",
    version="1.0.0"
)
class GreetingAgent(A2AServer):
    @skill(
        name="Greet",
        description="Respond to a greeting",
        tags=["greeting", "hello"]
    )
    def greet(self, name=None):
        """Respond to a greeting with a friendly message."""
        if name:
            return f"Hello, {name}! How can I help you today?"
        else:
            return "Hello there! How can I help you today?"
    
    def handle_task(self, task):
        #Extract message text
        message_data = task.message or {}
        content = message_data.get("content", {})
        text = content.get("text", "") if isinstance(content, dict) else ""
        
        #Check if it's a greeting
        greeting_words = ["hello", "hi", "hey", "greetings"]
        is_greeting = any(word in text.lower() for word in greeting_words)
        
        if is_greeting:
            #Extract name if present
            name = None
            if "my name is" in text.lower():
                name = text.lower().split("my name is")[1].strip()
                
            #Create greeting response
            greeting = self.greet(name)
            task.artifacts = [{
                "parts": [{"type": "text", "text": greeting}]
            }]
            task.status = TaskStatus(state=TaskState.COMPLETED)
        else:
            #Default response
            task.artifacts = [{
                "parts": [{"type": "text", "text": "I'm a greeting agent. Try saying hello!"}]
            }]
            task.status = TaskStatus(state=TaskState.COMPLETED)
            
        return task
    
#Run the server
if __name__ == "__main__":
    agent = GreetingAgent()
    run_server(agent, port=5000)