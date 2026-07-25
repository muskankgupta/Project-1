# import re


# class QueryAgent:

#     def generate_sql(self, question):

#         question = question.lower()


#         # Total revenue / sales
#         if "total revenue" in question or "total sales" in question:

#             quarter = re.search(r"quarter\s*(\d)", question)

#             if quarter:

#                 q = quarter.group(1)

#                 sql = f"""
#                 SELECT SUM(amount) AS total_revenue
#                 FROM amazon_sales
#                 WHERE QUARTER(order_date) = {q};
#                 """

#                 return sql


#             return """
#             SELECT SUM(amount) AS total_revenue
#             FROM amazon_sales;
#             """


#         # Count orders
#         elif "total orders" in question or "number of orders" in question:

#             return """
#             SELECT COUNT(order_id) AS total_orders
#             FROM amazon_sales;
#             """


#         # Average sales
#         elif "average sales" in question or "average revenue" in question:

#             return """
#             SELECT AVG(amount) AS average_sales
#             FROM amazon_sales;
#             """


#         # Category wise sales
#         elif "category sales" in question or "category revenue" in question:

#             return """
#             SELECT category,
#                    SUM(amount) AS total_sales
#             FROM amazon_sales
#             GROUP BY category;
#             """


#         # State wise sales
#         elif "state sales" in question:

#             return """
#             SELECT ship_state,
#                    SUM(amount) AS total_sales
#             FROM amazon_sales
#             GROUP BY ship_state
#             ORDER BY total_sales DESC;
#             """


#         else:

#             return None
class QueryAgent:

    def generate_query(self, intent):

        aggregation = intent.get("aggregation")
        column = intent.get("column")
        filters = intent.get("filters", {})

        # ✅ If missing required fields → STOP
        if not aggregation or not column:
            print("❌ Invalid intent:", intent)
            return None

        # ✅ Build SELECT
        sql = f"SELECT {aggregation}({column}) FROM amazon_sales"

        conditions = []

        # ✅ Filters
        if "quarter" in filters:
            conditions.append(f"QUARTER(order_date) = {filters['quarter']}")

        if "year" in filters:
            conditions.append(f"YEAR(order_date) = {filters['year']}")

        if "state" in filters:
            conditions.append(f"ship_state = '{filters['state']}'")

        if "category" in filters:
            conditions.append(f"category = '{filters['category']}'")

        # ✅ Add WHERE
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        # ✅ FINAL CHECK
        print("✅ Generated SQL:", sql)

        return sql   # 🚨 MUST be STRING