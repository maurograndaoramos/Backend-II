import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL
import uvicorn # Required to run the FastAPI app

# In-memory "database" for simplicity
mock_users_db = {
    1: {"id": 1, "name": "Alice Wonderland"},
    2: {"id": 2, "name": "Bob The Builder"},
}

@strawberry.type
class User:
    id: int
    name: str

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> User | None:
        print(f"Query: Fetching user with id: {id}")
        user_data = mock_users_db.get(id)
        if user_data:
            return User(id=user_data["id"], name=user_data["name"])
        return None

    @strawberry.field
    def all_users(self) -> list[User]:
        print("Query: Fetching all users")
        return [User(id=data["id"], name=data["name"]) for data in mock_users_db.values()]

@strawberry.type
class Mutation:
    @strawberry.mutation
    def update_user_name(self, user_id: int, new_name: str) -> User | None:
        print(f"Mutation: Updating user id {user_id} to name '{new_name}'")
        if user_id in mock_users_db:
            mock_users_db[user_id]["name"] = new_name
            updated_user_data = mock_users_db[user_id]
            return User(id=updated_user_data["id"], name=updated_user_data["name"])
        print(f"Mutation: User id {user_id} not found.")
        return None

    @strawberry.mutation
    def add_user(self, name: str) -> User:
        new_id = max(mock_users_db.keys() or [0]) + 1
        mock_users_db[new_id] = {"id": new_id, "name": name}
        print(f"Mutation: Added new user '{name}' with id {new_id}")
        return User(id=new_id, name=name)

# Create the GraphQL schema
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Create the FastAPI app and add the GraphQL route
graphql_app_instance = GraphQL(schema)
app = FastAPI()
app.add_route("/graphql", graphql_app_instance)
app.add_websocket_route("/graphql", graphql_app_instance) # For subscriptions if added later

if __name__ == "__main__":
    print("Starting FastAPI server for GraphQL exercise...")
    print("Access GraphQL UI at http://127.0.0.1:8000/graphql")
    print("\nExample Queries/Mutations:")
    print("""
    # Query for a single user:
    # query GetUser {
    #   user(id: 1) {
    #     id
    #     name
    #   }
    # }

    # Query for all users:
    # query GetAllUsers {
    #   allUsers {
    #     id
    #     name
    #   }
    # }

    # Mutation to update a user's name:
    # mutation UpdateName {
    #   updateUserName(userId: 1, newName: "Alice Smith") {
    #     id
    #     name
    #   }
    # }

    # Mutation to add a new user:
    # mutation AddNewUser {
    #   addUser(name: "Charlie Brown") {
    #     id
    #     name
    #   }
    # }
    """)
    uvicorn.run(app, host="127.0.0.1", port=8000)
