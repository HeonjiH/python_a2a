from python_a2a import A2AServer, skill, agent, run_server
from python_a2a import TaskStatus, TaskState
import re

@agent(
    name="Calculator",
    description="A simple calculator agent",
    version="1.0.0"
)
class CalculatorAgent(A2AServer):

    @skill(
        name="Add",
        description="Add two numbers",
        tags=["math", "addition"]
    )
    def add(self, a, b):
        """Add two numbers together."""
        return float(a) + float(b)

    @skill(
        name="Subtract",
        description="Subtract two numbers",
        tags=["math", "subtraction"]
    )
    def subtract(self, a, b):
        """Subtract b from a."""
        return float(a) - float(b)

    @skill(
        name="Multiply",
        description="Multiply two numbers",
        tags=["math", "multiplication"]
    )
    def multiply(self, a, b):
        """Multiply two numbers together."""
        return float(a) * float(b)

    @skill(
        name="Divide",
        description="Divide two numbers",
        tags=["math", "division"]
    )
    def divide(self, a, b):
        """Divide a by b."""
        return float(a) / float(b)

    def handle_task(self, task):
        # Extract message text
        message_data = task.message or {}
        content = message_data.get("content", {})
        text = content.get("text", "") if isinstance(content, dict) else ""

        # Find numbers in the text
        numbers = [float(n) for n in re.findall(r"[-+]?\d*\.?\d+", text)]

        # Default response
        response_text = "I can add, subtract, multiply, and divide numbers. Try asking something like 'add 5 and 3' or '10 divided by 2'."

        # Check for operation keywords
        if len(numbers) >= 2:
            a, b = numbers[0], numbers[1]

            if any(word in text.lower() for word in ["add", "plus", "sum", "+"]):
                result = self.add(a, b)
                response_text = f"{a} + {b} = {result}"
            elif any(word in text.lower() for word in ["subtract", "minus", "difference", "-"]):
                result = self.subtract(a, b)
                response_text = f"{a} - {b} = {result}"
            elif any(word in text.lower() for word in ["multiply", "times", "product", "*", "x"]):
                result = self.multiply(a, b)
                response_text = f"{a} × {b} = {result}"
            elif any(word in text.lower() for word in ["divide", "quotient", "/"]):
                if b != 0:
                    result = self.divide(a, b)
                    response_text = f"{a} ÷ {b} = {result}"
                else:
                    response_text = "Cannot divide by zero."

        # Create response artifact
        task.artifacts = [{
            "parts": [{"type": "text", "text": response_text}]
        }]
        task.status = TaskStatus(state=TaskState.COMPLETED)

        return task

# Run the server
if __name__ == "__main__":
    agent = CalculatorAgent()
    run_server(agent, port=5000)