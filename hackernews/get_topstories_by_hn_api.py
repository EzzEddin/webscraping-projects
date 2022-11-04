# https://github.com/HackerNews/API
import requests

url = 'https://hacker-news.firebaseio.com/v0'
top_stories_url = url + '/topstories.json'
top_stories = requests.get(top_stories_url).json()
print(len(top_stories)) # by default it returns the top 500 stories
stories = []
for story_id in top_stories:
    story_url = f"{url}/item/{story_id}.json"
    print(f"Fetching {story_url}")
    story_data = requests.get(story_url).json()
    stories.append({
        'url': story_data.get('url') if story_data.get('url') else None,
        'title': story_data.get('title') if story_data.get('title') else None,
        'score': story_data.get('score') if story_data.get('score') else None
    })
for story in stories:
    print(story)
