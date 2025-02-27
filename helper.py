import json

def get_all_posts():
    """
    Function fetches all posts from a JSON file and returns them.
    """
    with open("posts.json", "r") as fileobject:
        all_posts = json.load(fileobject)

        return all_posts


def save_all_posts_to_file(posts):
    """
    Function dumps all posts into a JSON file.
    """
    with open("posts.json", "w") as fileobj:
        json.dump(posts, fileobj)