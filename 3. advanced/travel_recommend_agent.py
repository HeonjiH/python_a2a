# travel_agent.py
from python_a2a import A2AServer, skill, agent, run_server, A2AClient
from python_a2a import TaskStatus, TaskState
import json

@agent(
    name="Travel Advisor",
    description="Provides travel recommendations based on weather",
    version="1.0.0"
)
class TravelAgent(A2AServer):

    def __init__(self):
        super().__init__()
        # Connect to the weather agent
        self.weather_client = A2AClient("http://localhost:5001")

        # Destination information
        self.destinations = {
            "new york": {"activities": ["Central Park", "Museums", "Broadway Shows"]},
            "london": {"activities": ["Big Ben", "Museums", "Thames River Cruise"]},
            "tokyo": {"activities": ["Temples", "Shopping", "Cherry Blossoms"]},
            "paris": {"activities": ["Eiffel Tower", "Louvre", "Cafes"]},
            "sydney": {"activities": ["Opera House", "Beaches", "Harbour Bridge"]},
            "cairo": {"activities": ["Pyramids", "Nile Cruise", "Markets"]},
            "rio": {"activities": ["Beaches", "Christ the Redeemer", "Samba"]},
            "bangkok": {"activities": ["Temples", "Street Food", "Markets"]},
            "moscow": {"activities": ["Red Square", "Museums", "Ballet"]},
            "dubai": {"activities": ["Shopping", "Desert Safari", "Burj Khalifa"]}
        }

    @skill(
        name="Recommend Destination",
        description="Recommend a destination based on weather preferences",
        tags=["travel", "recommendation"]
    )
    def recommend_destination(self, weather_pref, activity_pref=None):
        """
        Recommend a destination based on weather and activity preferences.

        Args:
            weather_pref: Weather preference (warm, cool, etc.)
            activity_pref: Optional activity preference

        Returns:
            Destination recommendation
        """
        # Get weather for all destinations
        destinations = []
        for dest in self.destinations.keys():
            try:
                weather = eval(self.weather_client.ask(f"What's the weather in {dest}?"))
                destinations.append({
                    "name": dest,
                    "weather": weather,
                    "activities": self.destinations[dest]["activities"]
                })
            except:
                # Skip if we can't get weather
                continue

        # Filter by weather preference
        filtered = []
        if weather_pref.lower() == "warm" or weather_pref.lower() == "hot":
            filtered = [d for d in destinations if d["weather"]["temp"] > 75]
        elif weather_pref.lower() == "cool" or weather_pref.lower() == "cold":
            filtered = [d for d in destinations if d["weather"]["temp"] < 60]
        elif weather_pref.lower() == "moderate" or weather_pref.lower() == "mild":
            filtered = [d for d in destinations if 60 <= d["weather"]["temp"] <= 75]
        else:
            filtered = destinations

        # Filter by activity preference if provided
        if activity_pref:
            activity_filtered = []
            for dest in filtered:
                for activity in dest["activities"]:
                    if activity_pref.lower() in activity.lower():
                        activity_filtered.append(dest)
                        break
            filtered = activity_filtered

        # Return results
        if filtered:
            return filtered
        else:
            return "No destinations match your preferences."

    def handle_task(self, task):
        # Extract message text
        message_data = task.message or {}
        content = message_data.get("content", {})
        text = content.get("text", "") if isinstance(content, dict) else ""

        # Initialize response
        response_text = "I can recommend destinations based on weather and activities. Try asking for recommendations for warm or cool places."

        # Extract preferences
        weather_pref = None
        activity_pref = None

        if "warm" in text.lower() or "hot" in text.lower():
            weather_pref = "warm"
        elif "cool" in text.lower() or "cold" in text.lower():
            weather_pref = "cool"
        elif "moderate" in text.lower() or "mild" in text.lower():
            weather_pref = "moderate"

        # Check for activities
        common_activities = ["beach", "museum", "food", "shopping", "nature", "cruise", "show"]
        for activity in common_activities:
            if activity in text.lower():
                activity_pref = activity
                break

        # Generate recommendations if preferences found
        if weather_pref:
            try:
                recommendations = self.recommend_destination(weather_pref, activity_pref)

                if isinstance(recommendations, str):
                    response_text = recommendations
                else:
                    response_text = f"Here are some {weather_pref} destinations"
                    if activity_pref:
                        response_text += f" with {activity_pref} activities"
                    response_text += ":\n\n"

                    for dest in recommendations[:3]:  # Limit to top 3
                        response_text += f"- {dest['name'].title()}: {dest['weather']['temp']}°F, {dest['weather']['condition']}\n"
                        response_text += f"  Activities: {', '.join(dest['activities'])}\n\n"
            except Exception as e:
                response_text = f"Sorry, I couldn't generate recommendations: {str(e)}"

        # Create response artifact
        task.artifacts = [{
            "parts": [{"type": "text", "text": response_text}]
        }]
        task.status = TaskStatus(state=TaskState.COMPLETED)

        return task

# Run the server
if __name__ == "__main__":
    agent = TravelAgent()
    run_server(agent, port=5002)