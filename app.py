from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json, os, uuid

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "inkwell-secret-2026")

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"users": {}, "posts": [], "comments": {}}
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def init_data():
    data = load_data()
    if not data["posts"]:
        data["posts"] = [
            {
                "id": "post1",
                "title": "Getting Started with Python Flask",
                "excerpt": "Learn how to build powerful web applications using Flask, Python's micro web framework.",
                "content": """Flask is a lightweight WSGI web application framework written in Python. It is designed to make getting started quick and easy, with the ability to scale up to complex applications.

Flask was created by Armin Ronacher and is based on the Werkzeug toolkit and Jinja2 template engine. It's called a micro-framework because it doesn't include an ORM, form validation, or authentication layer — you pick and add them yourself.

A minimal Flask application looks like this: just a few lines of Python and you have a running web server. The @app.route decorator maps URLs to Python functions. Templates let you separate HTML from Python logic cleanly.

Flask's extension ecosystem is mature. Flask-SQLAlchemy adds ORM support, Flask-Login handles authentication, Flask-WTF provides form handling. The microframework grows with your needs without imposing architecture on you.""",
                "author": "Admin",
                "author_id": "admin",
                "category": "Technology",
                "tags": ["Python", "Flask", "Backend"],
                "date": "June 10, 2026",
                "image_icon": "💻",
                "gradient": "grad-tech",
                "likes": 142,
                "liked_by": []
            },
            {
                "id": "post2",
                "title": "The Art of Slow Travel",
                "excerpt": "Why rushing between destinations robs you of the journey's true gifts — and how to slow down.",
                "content": """Slow travel is a philosophy, not just a pace. It's the deliberate choice to go deeper rather than wider — to spend three weeks in one city instead of three days in ten countries.

When you slow down, you start noticing the small things: the way morning light falls on old stone buildings, the rhythm of a neighborhood market, the conversations that only happen when you're not rushing to the next bus. You stop being a tourist and start becoming a temporary local.

Slow travel also forces you to be resourceful. Without a packed itinerary, you discover places not in guidebooks — the chai stall where locals gather at dawn, the bookshop run by an eccentric poet, the park where grandparents teach grandchildren to fly kites.

The environmental case is also compelling. Fewer flights, longer stays, lower carbon footprint. Slow travel aligns values with action.""",
                "author": "Admin",
                "author_id": "admin",
                "category": "Travel",
                "tags": ["Travel", "Mindfulness", "Culture"],
                "date": "June 8, 2026",
                "image_icon": "✈️",
                "gradient": "grad-travel",
                "likes": 98,
                "liked_by": []
            },
            {
                "id": "post3",
                "title": "Fermentation at Home: The Living Kitchen",
                "excerpt": "Kimchi, kefir, sourdough — why fermented foods are having a moment and how to start.",
                "content": """Fermentation is one of humanity's oldest food technologies, and it's experiencing a remarkable renaissance. From kimchi to kombucha, kefir to sourdough, people are rediscovering the magic of letting microbes do the work.

The health case is compelling: fermented foods are rich in probiotics that support gut health, improve digestion, and may even influence mood via the gut-brain axis. But the real reason to start fermenting at home is simpler — it's delicious and endlessly fascinating.

Starting is easier than you think. Lacto-fermented vegetables require only salt, water, and a jar. Slice your vegetables, pack them tightly, submerge in a 2% salt brine, and wait. Within days, bubbles will tell you the lactobacillus bacteria are at work.

Sourdough requires a starter — a live culture of wild yeast and bacteria. Feed it flour and water daily, and within a week it'll be ready to leaven bread. The process demands patience and rewards it.""",
                "author": "Admin",
                "author_id": "admin",
                "category": "Food",
                "tags": ["Cooking", "Health", "DIY"],
                "date": "June 5, 2026",
                "image_icon": "🍽️",
                "gradient": "grad-food",
                "likes": 76,
                "liked_by": []
            },
            {
                "id": "post4",
                "title": "Digital Minimalism: Reclaiming Your Attention",
                "excerpt": "The case for intentionally reducing your digital footprint — and the tools to do it.",
                "content": """Digital minimalism is not about rejecting technology. It's about being intentional about which technologies you allow into your life and how you use them.

Cal Newport, who popularized the term, defines it as a philosophy of technology use where you focus your online time on a small number of carefully selected activities that strongly support things you value, and happily miss out on everything else.

The starting point is a digital declutter: a 30-day break from optional technologies, then a careful reintroduction based on what you actually missed. Most people find they missed very little and gained a lot — time, focus, a renewed ability to be bored without reaching for a phone.

Practical tools help: grayscale mode on your phone makes it less visually compelling. App timers create friction before opening social media. Notification silencing protects deep work. But tools alone aren't enough — you need to fill recovered time with genuinely meaningful activities.""",
                "author": "Admin",
                "author_id": "admin",
                "category": "Lifestyle",
                "tags": ["Productivity", "Wellness", "Tech"],
                "date": "June 2, 2026",
                "image_icon": "🌿",
                "gradient": "grad-life",
                "likes": 211,
                "liked_by": []
            },
            {
                "id": "post5",
                "title": "Monsoon Photography: Light After Rain",
                "excerpt": "How the rainy season creates dramatic and beautiful photographic opportunities.",
                "content": """Monsoon season is a gift to photographers. Rain washes away dust and haze, leaving the air crystal clear. Wet surfaces reflect light in extraordinary ways. Clouds create soft, even lighting that flatters almost any subject.

The golden rule of monsoon photography: go out immediately after the rain stops. That 30-minute window offers the best conditions — clean air, dramatic skies clearing, reflections everywhere, people and animals resuming activity.

Water reflections are the monsoon photographer's best friend. Puddles, flooded fields, wet roads — all become mirrors. Frame your shot so both the subject and its reflection fill the frame.

For landscapes, wait for crepuscular rays — those dramatic beams of light that break through clouds after rain. They're most common in early morning and late afternoon.""",
                "author": "Admin",
                "author_id": "admin",
                "category": "Photography",
                "tags": ["Photography", "Art", "Nature"],
                "date": "May 30, 2026",
                "image_icon": "📷",
                "gradient": "grad-photo",
                "likes": 134,
                "liked_by": []
            },
            {
                "id": "post6",
                "title": "Learning Sanskrit: Gateway to Ancient Texts",
                "excerpt": "Why a growing number of young people are picking up one of the world's oldest languages.",
                "content": """Sanskrit, often called the mother of many languages, is experiencing an unlikely revival. Driven by curiosity about Vedic texts, yoga philosophy, and computational linguistics, a new generation is sitting down to learn Devanagari script.

The benefits go beyond access to ancient literature. Sanskrit is extraordinarily precise — its grammar, codified by Pāṇini around 500 BCE, is so rigorous that it has been studied by modern linguists as a model for computational language processing.

For practitioners of yoga or Ayurveda, learning Sanskrit unlocks primary sources. Sutras that seem mysterious in translation reveal new depths in the original.

Modern resources make starting easier than ever. Apps have introduced Sanskrit courses. The Samskrita Bharati organization runs spoken Sanskrit camps across India. Start with the alphabet — Devanagari is phonetically consistent.""",
                "author": "Admin",
                "author_id": "admin",
                "category": "Education",
                "tags": ["Language", "Culture", "History"],
                "date": "May 27, 2026",
                "image_icon": "📚",
                "gradient": "grad-edu",
                "likes": 87,
                "liked_by": []
            }
        ]
        data["comments"] = {
            "post1": [
                {"id": "c1", "author": "Priya S", "text": "Really helpful intro! The Flask routing section was especially clear.", "date": "June 11, 2026"},
                {"id": "c2", "author": "Arjun M", "text": "I've been struggling with templates. This clears things up perfectly.", "date": "June 11, 2026"}
            ],
            "post2": [
                {"id": "c3", "author": "Meena J", "text": "This resonates deeply. Spent a month in Oaxaca and it changed how I see travel.", "date": "June 9, 2026"}
            ],
            "post4": [
                {"id": "c4", "author": "Priya S", "text": "The grayscale mode tip alone changed everything for me.", "date": "June 3, 2026"}
            ]
        }
        save_data(data)

# ──────────────────────────────────────────
# AUTH ROUTES
# ──────────────────────────────────────────
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = load_data()
        username = request.form["username"].strip()
        email = request.form["email"].strip().lower()
        password = request.form["password"]
        if username in data["users"]:
            flash("Username already taken.", "error")
            return render_template("register.html")
        data["users"][username] = {
            "username": username,
            "email": email,
            "password": generate_password_hash(password),
            "joined": datetime.now().strftime("%B %d, %Y"),
            "bio": ""
        }
        save_data(data)
        session["user"] = username
        flash("Account created! Welcome to Inkwell.", "success")
        return redirect(url_for("index"))
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = load_data()
        username = request.form["username"].strip()
        password = request.form["password"]
        user = data["users"].get(username)
        if user and check_password_hash(user["password"], password):
            session["user"] = username
            flash(f"Welcome back, {username}!", "success")
            return redirect(url_for("index"))
        flash("Invalid username or password.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("index"))

# ──────────────────────────────────────────
# MAIN ROUTES
# ──────────────────────────────────────────
@app.route("/")
def index():
    data = load_data()
    category = request.args.get("category", "All")
    search = request.args.get("search", "").lower()
    posts = data["posts"]
    if category != "All":
        posts = [p for p in posts if p["category"] == category]
    if search:
        posts = [p for p in posts if search in p["title"].lower() or search in p["excerpt"].lower()]
    categories = ["All", "Technology", "Travel", "Food", "Lifestyle", "Photography", "Education"]
    total_likes = sum(p["likes"] for p in data["posts"])
    total_comments = sum(len(v) for v in data["comments"].values())
    return render_template("index.html", posts=posts, categories=categories,
                           active_cat=category, search=search,
                           total_posts=len(data["posts"]),
                           total_likes=total_likes,
                           total_comments=total_comments,
                           user=session.get("user"))

@app.route("/post/<post_id>")
def post_detail(post_id):
    data = load_data()
    post = next((p for p in data["posts"] if p["id"] == post_id), None)
    if not post:
        return redirect(url_for("index"))
    comments = data["comments"].get(post_id, [])
    user = session.get("user")
    liked = user in post.get("liked_by", []) if user else False
    return render_template("post_detail.html", post=post, comments=comments, user=user, liked=liked)

@app.route("/create", methods=["GET", "POST"])
def create_post():
    if not session.get("user"):
        flash("Login required to create posts.", "error")
        return redirect(url_for("login"))
    if request.method == "POST":
        data = load_data()
        post_id = "post_" + str(uuid.uuid4())[:8]
        content = request.form["content"]
        gradients = {"Technology":"grad-tech","Travel":"grad-travel","Food":"grad-food",
                     "Lifestyle":"grad-life","Photography":"grad-photo","Education":"grad-edu"}
        icons = {"Technology":"💻","Travel":"✈️","Food":"🍽️","Lifestyle":"🌿","Photography":"📷","Education":"📚"}
        cat = request.form["category"]
        post = {
            "id": post_id,
            "title": request.form["title"],
            "excerpt": content[:130] + "…" if len(content) > 130 else content,
            "content": content,
            "author": session["user"],
            "author_id": session["user"],
            "category": cat,
            "tags": [t.strip() for t in request.form.get("tags","").split(",") if t.strip()],
            "date": datetime.now().strftime("%B %d, %Y"),
            "image_icon": icons.get(cat, "📝"),
            "gradient": gradients.get(cat, "grad-tech"),
            "likes": 0,
            "liked_by": []
        }
        data["posts"].insert(0, post)
        data["comments"][post_id] = []
        save_data(data)
        flash("Post published successfully!", "success")
        return redirect(url_for("post_detail", post_id=post_id))
    return render_template("create_post.html", user=session.get("user"))

@app.route("/post/<post_id>/comment", methods=["POST"])
def add_comment(post_id):
    if not session.get("user"):
        flash("Login required to comment.", "error")
        return redirect(url_for("post_detail", post_id=post_id))
    text = request.form.get("text", "").strip()
    if not text:
        return redirect(url_for("post_detail", post_id=post_id))
    data = load_data()
    if post_id not in data["comments"]:
        data["comments"][post_id] = []
    data["comments"][post_id].append({
        "id": str(uuid.uuid4())[:8],
        "author": session["user"],
        "text": text,
        "date": datetime.now().strftime("%B %d, %Y")
    })
    save_data(data)
    return redirect(url_for("post_detail", post_id=post_id) + "#comments")

@app.route("/post/<post_id>/like", methods=["POST"])
def like_post(post_id):
    if not session.get("user"):
        return jsonify({"error": "login required"}), 401
    data = load_data()
    user = session["user"]
    for post in data["posts"]:
        if post["id"] == post_id:
            if user in post.get("liked_by", []):
                post["liked_by"].remove(user)
                post["likes"] = max(0, post["likes"] - 1)
                liked = False
            else:
                post.setdefault("liked_by", []).append(user)
                post["likes"] += 1
                liked = True
            save_data(data)
            return jsonify({"likes": post["likes"], "liked": liked})
    return jsonify({"error": "not found"}), 404

@app.route("/profile")
def profile():
    if not session.get("user"):
        return redirect(url_for("login"))
    data = load_data()
    user = session["user"]
    user_info = data["users"].get(user, {})
    my_posts = [p for p in data["posts"] if p["author_id"] == user]
    total_likes = sum(p["likes"] for p in my_posts)
    total_comments = sum(len(data["comments"].get(p["id"], [])) for p in my_posts)
    return render_template("profile.html", user=user, user_info=user_info,
                           my_posts=my_posts, total_likes=total_likes,
                           total_comments=total_comments)

@app.route("/post/<post_id>/delete", methods=["POST"])
def delete_post(post_id):
    if not session.get("user"):
        return redirect(url_for("login"))
    data = load_data()
    post = next((p for p in data["posts"] if p["id"] == post_id), None)
    if post and (post["author_id"] == session["user"] or session["user"] == "admin"):
        data["posts"] = [p for p in data["posts"] if p["id"] != post_id]
        data["comments"].pop(post_id, None)
        save_data(data)
        flash("Post deleted.", "success")
    return redirect(url_for("profile"))

if __name__ == "__main__":
    init_data()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
