from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/blogDB"
mongo = PyMongo(app)
db = mongo.db.posts

# Home route
@app.route('/')
def home():
    return "Welcome to the Blog API!"

# Create a new blog post
@app.route('/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    post_id = db.insert_one(data).inserted_id
    return jsonify({"message": "Post created", "id": str(post_id)}), 201

# Read all blog posts
@app.route('/posts', methods=['GET'])
def get_posts():
    posts = []
    for post in db.find():
        posts.append({"id": str(post["_id"]), "title": post["title"], "content": post["content"]})
    return jsonify(posts), 200

# Update a blog post
@app.route('/posts/<id>', methods=['PUT'])
def update_post(id):
    data = request.get_json()
    db.update_one({"_id": ObjectId(id)}, {"$set": data})
    return jsonify({"message": "Post updated"}), 200

# Delete a blog post
@app.route('/posts/<id>', methods=['DELETE'])
def delete_post(id):
    db.delete_one({"_id": ObjectId(id)})
    return jsonify({"message": "Post deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
