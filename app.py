from flask import Flask, url_for
from flask import request, render_template, redirect
import json

app = Flask(__name__)
POST_ID = 0

@app.route('/add', methods=['GET', 'POST'])
def add():
    global POST_ID
    with open("posts.json", "r") as fileobject:
        all_posts = json.load(fileobject)

    if request.method == 'POST':
        action = request.form.get("action")

        if action == "add":
            title = request.form.get("post-title")
            content = request.form.get("post-body")
            author = request.form.get("post-author")
            POST_ID += 1

            new_post = {"id": POST_ID,
                         "author": author,
                           "title": title,
                             "content": content}
            
            all_posts.append(new_post)
            print(all_posts)
            with open("posts.json", "w") as fileobj:
                json.dump(all_posts, fileobj)
            
            return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    updated_posts  = []
    with open("posts.json", "r") as fileobject:
        all_posts = json.load(fileobject)

    for post in all_posts:
        if post["id"] != post_id:
            updated_posts.append(post)
    
    with open("posts.json", "w") as fileobj:
        json.dump(updated_posts, fileobj)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Fetch the blog posts from the JSON file
    with open("posts.json", "r") as fileobject:
        all_posts = json.load(fileobject)

    post = [post for post in all_posts if post["id"] == post_id]
    if post is None:
        # Post not found
        return "Post not found", 404

    if request.method == 'POST':
        # Update the post in the JSON file
        # Redirect back to index
        action = request.form.get("action")

        if action == "update":
            title = request.form.get("post-title")
            content = request.form.get("post-body")
            author = request.form.get("post-author")
        
            for post in all_posts:
                if post['id'] == post_id:
                    post["author"] = author
                    post["title"] = title
                    post["content"] = content

            with open("posts.json", "w") as fileobj:
                json.dump(all_posts, fileobj)
            
            return redirect(url_for('index'))

    # Else, it's a GET request
    # So display the update.html page
    return render_template('update.html', post=post[0])

@app.route('/')
def index():
    while True:
        try:
            with open("posts.json", "r") as fileobject:
                posts = json.load(fileobject)
                break
        except FileNotFoundError:
            with open("posts.json", 'w') as fileobject:
                fileobject.write("[]")
 

    return render_template("index.html", posts=posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)