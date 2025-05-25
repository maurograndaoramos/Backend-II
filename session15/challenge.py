# Challenge Session 15: Advanced CrewAI Agent with External API Enrichment
# Problem: Develop an AI agent that can handle complex queries and respond with relevant information, possibly using external APIs for data enrichment.
# Hint: Implement a more sophisticated response logic that can parse and respond to structured queries.

import random

class AdvancedAgent:
    def __init__(self):
        pass

    def fetch_weather(self, city):
        # Simulação de chamada a API externa
        temp = random.randint(10, 30)
        return f"The current temperature in {city} is {temp}°C."

    def respond(self, query):
        query = query.lower()
        if "weather" in query and "in" in query:
            parts = query.split("in")
            city = parts[-1].strip().capitalize()
            return self.fetch_weather(city)
        elif "history" in query:
            return "You asked about your query history. (Simulated response)"
        elif "recommend" in query:
            return "I recommend studying Python concurrency for backend excellence."
        else:
            return "Sorry, I can't answer that complex query."

if __name__ == "__main__":
    agent = AdvancedAgent()
    queries = [
        "What's the weather in Lisbon?",
        "Show me my history",
        "Can you recommend something?",
        "Unknown complex query"
    ]
    for q in queries:
        print(f"Query: {q} -> Response: {agent.respond(q)}")

