from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import threading
import logging

from models import (
    init_db, upsert_product, get_products, get_product, get_price_history,
    toggle_favorite, update_notes, delete_product,
    create_task, update_task, get_tasks, get_stats
)
from parser import get_product_by_id, search_products, get_seller_products

app = Flask(__name__)
app.secret_key = "wb-admin-secret-2024"
logging.basicConfig(level=logging.INFO)

# ─── Background parse runner ────────────────────────────────────────────────

def _run_parse(task_id: int, task_type: str, query: str):
    try:
        products = []
        if task_type == "article":
            p = get_product_by_id(int(query))
            products = [p] if p else []
        elif task_type == "search":
            products = search_products(query, limit=30)
        elif task_type == "seller":
            products = get_seller_products(int(query), limit=30)

        for p in products:
            upsert_product(p)
        update_task(task_id, "done", len(products))
    except Exception as e:
        update_task(task_id, "error", 0, str(e))


# ─── Routes ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    stats = get_stats()
    tasks = get_tasks(5)
    return render_template("index.html", stats=stats, tasks=tasks)


@app.route("/products")
def products():
    search = request.args.get("q", "")
    sort = request.args.get("sort", "updated_at")
    order = request.args.get("order", "DESC")
    page = int(request.args.get("page", 1))
    favorites = request.args.get("favorites") == "1"
    items, total = get_products(search, sort, order, page, 20, favorites)
    pages = (total + 19) // 20
    return render_template("products.html",
        products=items, total=total, page=page, pages=pages,
        search=search, sort=sort, order=order, favorites=favorites
    )


@app.route("/product/<int:article>")
def product_detail(article):
    p = get_product(article)
    if not p:
        flash("Товар не найден", "error")
        return redirect(url_for("products"))
    history = get_price_history(article)
    return render_template("product_detail.html", product=p, history=history)


@app.route("/product/<int:article>/favorite", methods=["POST"])
def toggle_fav(article):
    toggle_favorite(article)
    return jsonify({"ok": True})


@app.route("/product/<int:article>/notes", methods=["POST"])
def save_notes(article):
    notes = request.json.get("notes", "")
    update_notes(article, notes)
    return jsonify({"ok": True})


@app.route("/product/<int:article>/delete", methods=["POST"])
def del_product(article):
    delete_product(article)
    return jsonify({"ok": True})


@app.route("/parse", methods=["GET", "POST"])
def parse_page():
    if request.method == "POST":
        task_type = request.form.get("type")
        query = request.form.get("query", "").strip()
        if not query:
            flash("Введите запрос", "error")
        else:
            task_id = create_task(task_type, query)
            t = threading.Thread(target=_run_parse, args=(task_id, task_type, query), daemon=True)
            t.start()
            flash(f"Задача #{task_id} запущена", "success")
        return redirect(url_for("parse_page"))

    tasks = get_tasks(30)
    return render_template("parse.html", tasks=tasks)


@app.route("/api/stats")
def api_stats():
    return jsonify(get_stats())


@app.route("/api/tasks")
def api_tasks():
    return jsonify(get_tasks(10))


@app.route("/api/products")
def api_products():
    search = request.args.get("q", "")
    items, total = get_products(search, page=1, per_page=100)
    return jsonify({"total": total, "products": items})


if __name__ == "__main__":
    init_db()
    print("\n🚀 Wildberries Admin запущен: http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)
