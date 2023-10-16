from fastapi import FastAPI, HTTPException, Query
import instaloader

app = FastAPI()

@app.get('/instadata')
async def get_instagram_data(username: str = Query(..., title="Instagram Username")):
    try:
        # Create an Instaloader instance
        L = instaloader.Instaloader()

        # Replace 'username' with the actual Instagram username
        profile = instaloader.Profile.from_username(L.context, username)

        total_likes = 0
        total_comments = 0
        total_posts = 0
        followers = profile.followers

        # Iterate through the user's posts and calculate total likes, comments, and count of posts
        for post in profile.get_posts():
            total_likes += post.likes
            total_comments += post.comments
            total_posts += 1

        engagement_rate = ((total_likes + total_comments) / (total_posts * followers)) * 100

        # Round off the engagement rate to two decimal places
        engagement_rate = round(engagement_rate, 2)

        # Return the Instagram data as JSON
        return {
            'username': username,
            'total_likes': total_likes,
            'total_comments': total_comments,
            'total_posts': total_posts,
            'followers': followers,
            'engagement_rate': engagement_rate
        }

    except instaloader.exceptions.ProfileNotExistsException:
        raise HTTPException(status_code=404, detail='User not found')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
