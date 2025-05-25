import strawberry
from fastapi import FastAPI, Request, HTTPException
from strawberry.asgi import GraphQL
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional, Any
import uvicorn

# --- In-memory "database" ---
mock_posts_db = {
    1: {"id": 1, "title": "GraphQL Basics", "content": "Learn the fundamentals of GraphQL.", "author_id": 1},
    2: {"id": 2, "title": "Advanced GraphQL", "content": "Deep dive into GraphQL.", "author_id": 1},
    3: {"id": 3, "title": "Python Tips", "content": "Useful tips for Python developers.", "author_id": 2},
    4: {"id": 4, "title": "Intro to FastAPI", "content": "Building APIs with FastAPI.", "author_id": 1},
}

mock_users_db = {
    1: {"id": 1, "name": "Alice Wonderland", "email": "alice@example.com"},
    2: {"id": 2, "name": "Bob The Builder", "email": "bob@example.com"},
}

# --- Strawberry Types ---
@strawberry.type
class Post:
    id: int
    title: str
    content: str
    author_id: int # Keep it simple for now, resolve author separately

    @strawberry.field
    def author(self) -> "User": # Forward reference for User
        print(f"Post {self.id}: Resolving author with id {self.author_id}")
        user_data = mock_users_db.get(self.author_id)
        if user_data:
            return User(id=user_data["id"], name=user_data["name"], email=user_data["email"])
        raise ValueError(f"Author with id {self.author_id} not found for post {self.id}")

@strawberry.type
class User:
    id: int
    name: str
    email: str

    @strawberry.field
    def posts(self) -> List[Post]:
        print(f"User {self.id}: Resolving posts")
        user_posts = [
            Post(id=data["id"], title=data["title"], content=data["content"], author_id=data["author_id"])
            for data in mock_posts_db.values()
            if data["author_id"] == self.id
        ]
        return user_posts

@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> Optional[User]:
        user_data = mock_users_db.get(id)
        if user_data:
            return User(**user_data)
        return None

    @strawberry.field
    def post(self, id: int) -> Optional[Post]:
        post_data = mock_posts_db.get(id)
        if post_data:
            return Post(**post_data)
        return None

    @strawberry.field
    def all_users(self) -> List[User]:
        return [User(**data) for data in mock_users_db.values()]

    @strawberry.field
    def all_posts(self) -> List[Post]:
        return [Post(**data) for data in mock_posts_db.values()]

# --- Authentication Logic (Simplified) ---
async def get_context(request: Request):
    # Simulate token authentication
    # In a real app, you'd parse and validate a JWT or session token
    auth_token = request.headers.get("Authorization")
    user = None
    if auth_token and auth_token.startswith("Bearer "):
        token_value = auth_token.split(" ")[1]
        # Simple mock: if token is "admin_token", user is Alice (ID 1)
        if token_value == "admin_token_alice":
            user = mock_users_db.get(1) 
        elif token_value == "user_token_bob":
            user = mock_users_db.get(2)
    
    return {"request": request, "current_user": user}


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_post(self, title: str, content: str, info: strawberry.Info) -> Post:
        current_user_data = info.context.get("current_user")
        if not current_user_data:
            raise PermissionError("Authentication required to create a post.") # Strawberry handles this as an error

        author_id = current_user_data["id"]
        new_id = max(mock_posts_db.keys() or [0]) + 1
        new_post_data = {"id": new_id, "title": title, "content": content, "author_id": author_id}
        mock_posts_db[new_id] = new_post_data
        print(f"Mutation: User {author_id} created post '{title}' (id: {new_id})")
        return Post(**new_post_data)

    @strawberry.mutation
    def update_post_title(self, post_id: int, new_title: str, info: strawberry.Info) -> Optional[Post]:
        current_user_data = info.context.get("current_user")
        if not current_user_data:
            raise PermissionError("Authentication required.")

        post_data = mock_posts_db.get(post_id)
        if not post_data:
            print(f"Mutation: Post id {post_id} not found.")
            return None # Or raise an error: raise ValueError("Post not found")

        # Simple authorization: only author can update
        if post_data["author_id"] != current_user_data["id"]:
            raise PermissionError("You are not authorized to update this post.")
        
        post_data["title"] = new_title
        print(f"Mutation: User {current_user_data['id']} updated post {post_id} title to '{new_title}'")
        return Post(**post_data)

# --- Schema and App Setup ---
schema = strawberry.Schema(query=Query, mutation=Mutation)

# Using GraphQLRouter for context dependency injection
graphql_app_router = GraphQLRouter(schema, context_getter=get_context)

app = FastAPI()
app.include_router(graphql_app_router, prefix="/graphql")


if __name__ == "__main__":
    print("Starting FastAPI server for Advanced GraphQL challenge...")
    print("Access GraphQL UI at http://127.0.0.1:8001/graphql")
    print("\nTo test authenticated mutations, include an 'Authorization' header.")
    print("Example: 'Authorization: Bearer admin_token_alice' (for Alice, user ID 1)")
    print("Example: 'Authorization: Bearer user_token_bob' (for Bob, user ID 2)")
    print("\nExample Queries/Mutations:")
    print("""
    # Query for a user and their posts (nested query):
    # query GetUserWithPosts {
    #   user(id: 1) {
    #     id
    #     name
    #     email
    #     posts {
    #       id
    #       title
    #       content
    #     }
    #   }
    # }

    # Query for a post and its author (nested query):
    # query GetPostWithAuthor {
    #   post(id: 1) {
    #     id
    #     title
    #     author {
    #       id
    #       name
    #     }
    #   }
    # }

    # Mutation to create a post (requires 'Authorization' header):
    # mutation CreateNewPost {
    #   createPost(title: "My New Adventure", content: "It was a dark and stormy night...") {
    #     id
    #     title
    #     author {
    #       name
    #     }
    #   }
    # }
    
    # Mutation to update a post title (requires 'Authorization' header and user must be author):
    # mutation UpdateExistingPostTitle {
    #   updatePostTitle(postId: 1, newTitle: "GraphQL Basics Revised") {
    #     id
    #     title
    #     content
    #   }
    # }
    """)
    uvicorn.run(app, host="127.0.0.1", port=8001)
