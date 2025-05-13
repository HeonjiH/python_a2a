# weather_agent.py
from python_a2a import A2AServer, skill, agent, run_server
from python_a2a import TaskStatus, TaskState
import random

# 에이전트 카드
@agent(
    name="Weather API",
    description="Provides weather information for locations",
    version="1.0.0"
)
class WeatherAgent(A2AServer):

    def __init__(self):
        super().__init__()
        # Mock weather data
        self.weather_data = {
            "new york": {"temp": 72, "condition": "Sunny", "humidity": 45},
            "london": {"temp": 60, "condition": "Cloudy", "humidity": 80},
            "tokyo": {"temp": 75, "condition": "Rainy", "humidity": 85},
            "paris": {"temp": 68, "condition": "Partly Cloudy", "humidity": 60},
            "sydney": {"temp": 82, "condition": "Sunny", "humidity": 50},
            "cairo": {"temp": 95, "condition": "Sunny", "humidity": 30},
            "rio": {"temp": 88, "condition": "Sunny", "humidity": 70},
            "bangkok": {"temp": 90, "condition": "Thunderstorms", "humidity": 95},
            "moscow": {"temp": 45, "condition": "Snowy", "humidity": 70},
            "dubai": {"temp": 105, "condition": "Sunny", "humidity": 20}
        }

    @skill(
        name="Get Weather",
        description="Get current weather for a location",
        tags=["weather", "current"]
    )
    def get_weather(self, location):
        """
        Get the current weather for a location.

        Args:
            location: The location to get weather for

        Returns:
            Weather information
        """
        location = location.lower()
        if location in self.weather_data:
            return self.weather_data[location]

        # Generate random weather for unknown locations
        return {
            "temp": random.randint(50, 90),
            "condition": random.choice(["Sunny", "Cloudy", "Rainy", "Partly Cloudy"]),
            "humidity": random.randint(30, 90)
        }

    @skill(
        name="Get Forecast",
        description="Get 5-day forecast for a location",
        tags=["weather", "forecast"]
    )
    def get_forecast(self, location):
        """
        Get a 5-day forecast for a location.

        Args:
            location: The location to get forecast for

        Returns:
            5-day forecast
        """
        base_weather = self.get_weather(location)

        # Generate a simple 5-day forecast
        forecast = []
        for day in range(1, 6):
            temp_change = random.randint(-10, 10)
            forecast.append({
                "day": day,
                "temp": base_weather["temp"] + temp_change,
                "condition": random.choice(["Sunny", "Cloudy", "Rainy", "Partly Cloudy"]),
                "humidity": base_weather["humidity"] + random.randint(-20, 20)
            })

        return forecast

    def handle_task(self, task):
        # Extract message text
        message_data = task.message or {}
        content = message_data.get("content", {})
        text = content.get("text", "") if isinstance(content, dict) else ""

        # Initialize response
        response_text = "I can provide weather information. Try asking for the weather or forecast in a specific location."

        # Check for location in the query
        location = None
        if "in" in text.lower():
            location = text.lower().split("in", 1)[1].strip().rstrip("?.")

        # Check for forecast vs current weather
        if location:
            if "forecast" in text.lower():
                forecast = self.get_forecast(location)
                response_text = f"5-day forecast for {location.title()}:\n"
                for day in forecast:
                    response_text += f"Day {day['day']}: {day['temp']}°F, {day['condition']}, {day['humidity']}% humidity\n"
            else:
                weather = self.get_weather(location)
                response_text = f"Current weather in {location.title()}: {weather['temp']}°F, {weather['condition']}, {weather['humidity']}% humidity"

        # Create response artifact
        task.artifacts = [{
            "parts": [{"type": "text", "text": response_text}]
        }]
        task.status = TaskStatus(state=TaskState.COMPLETED)

        return task

# Run the server
if __name__ == "__main__":
    agent = WeatherAgent()
    run_server(agent, port=5001)