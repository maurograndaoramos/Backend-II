# Challenge Session 14: CrewAI Agent with Keyword-Based Responses
# Problem: Enhance the agent to handle multiple queries with different responses based on keywords.
# Hint: Use conditional statements or a mapping dictionary.

class KeywordAgent:
    def __init__(self):
        self.responses = {
            "hello": "Hi! How can I help you?",
            "weather": "The weather is sunny.",
            "bye": "Goodbye!",
        }

    def respond(self, query):
        for keyword, response in self.responses.items():
            if keyword in query.lower():
                return response
        return "Sorry, I don't understand."

if __name__ == "__main__":
    agent = KeywordAgent()
    queries = ["Hello", "Tell me the weather", "Bye", "Unknown"]
    for q in queries:
        print(f"Query: {q} -> Response: {agent.respond(q)}")

