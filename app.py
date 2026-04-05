from flask import Flask, render_template_string
import sqlite3
import pandas as pd

app = Flask(__name__)

@app.route("/")
def index():
    conn = sqlite3.connect("data.db")
    orders = pd.read_sql("SELECT * FROM orders", conn)
    summary = pd.read_sql("SELECT * FROM summary", conn)
    conn.close()
    
    html = """
    <h1>📊 订单数据列表</h1>
    {{orders|safe}}
    <h1>🌍 区域金额平均值</h1>
    {{summary|safe}}
    """
    return render_template_string(html, orders=orders.to_html(), summary=summary.to_html())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)