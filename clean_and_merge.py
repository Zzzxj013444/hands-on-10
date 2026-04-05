import pandas as pd
import sqlite3

# 读取数据
order = pd.read_csv("data/order.txt")
customer = pd.read_csv("data/customer.txt")

# 去重
order = order.drop_duplicates()
customer = customer.drop_duplicates()

# 货币转换为人民币
def convert_currency(row):
    rate = {"USD":6.9, "EUR":7.5, "CNY":1.0, "JPY":0.05}
    return row["amount"] * rate[row["currency"]]

order["amount_cny"] = order.apply(convert_currency, axis=1)

# 合并订单和客户数据
merged = pd.merge(order, customer, on="customer_id")

# 保存到SQLite数据库
conn = sqlite3.connect("data.db")
merged.to_sql("orders", conn, if_exists="replace", index=False)

# 生成区域汇总表
summary = merged.groupby("region")["amount_cny"].mean().reset_index()
summary.to_sql("summary", conn, if_exists="replace", index=False)

conn.close()
print("✅ 数据处理完成！数据库已更新")