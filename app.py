from flask import Flask, url_for
from flask import request, render_template, redirect
import helper

app = Flask(__name__)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Function adds a new post to a post database. 
    """
    all_posts = helper.get_all_posts()

    if not all_posts:
        post_id = 0
    else:
        all_ids = [post["id"] for post in all_posts]
        post_id = max(all_ids)

    if request.method == 'POST':
        action = request.form.get("action")

        if action == "add":
            title = request.form.get("post-title")
            content = request.form.get("post-body")
            author = request.form.get("post-author")
            post_id += 1

            new_post = {"id": post_id,
                         "author": author,
                           "title": title,
                             "content": content}
            
            all_posts.append(new_post)
            helper.save_all_posts_to_file(all_posts)
            
            return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """
    Function deletes a post with a specified id from a database.
    """
    updated_posts  = []
    all_posts = helper.get_all_posts()

    for post in all_posts:
        if post["id"] != post_id:
            updated_posts.append(post)
    
    helper.save_all_posts_to_file(updated_posts)

    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """
    Function updates a post of a specified id. 
    Once changes are submitted, redirects the user back to main page.
    """
    all_posts = helper.get_all_posts()

    post = [post for post in all_posts if post["id"] == post_id]
    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        action = request.form.get("action")

        if action == "update":
            title = request.form.get("post-title")
            content = request.form.get("post-body")
            author = request.form.get("post-author")
        
            for post in all_posts:
                if post["id"] == post_id:
                    post["author"] = author
                    post["title"] = title
                    post["content"] = content

            helper.save_all_posts_to_file(all_posts)
            
            return redirect(url_for('index'))

    return render_template('update.html', post=post[0])


@app.route('/')
def index():
    """
    Function fetches all the posts from a database and renders main page.
    """
    while True:
        try:
            posts = helper.get_all_posts()
            break
        except FileNotFoundError:
            with open("posts.json", 'w') as fileobject:
                fileobject.write("[]")
 
    return render_template("index.html", posts=posts)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)