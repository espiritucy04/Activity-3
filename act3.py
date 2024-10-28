from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

@app.get("/detailed_post/{userID}")
def get_detailed_post(userID: int):
    # Step 1: Get posts for the user
    posts_response = requests.get(f"https://jsonplaceholder.typicode.com/users/{userID}/posts")
    if posts_response.status_code != 200:
        raise HTTPException(status_code=404, detail="User not found or API error")

    posts = posts_response.json()
    detailed_posts = []

    # Step 2: For each post, get comments and combine
    for post in posts:
        post_id = post["id"]
        comments_response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}/comments")
        
        if comments_response.status_code == 200:
            post["comments"] = comments_response.json()
        else:
            post["comments"] = []  # Empty comments if fetch fails

        detailed_posts.append(post)

    return detailed_posts
