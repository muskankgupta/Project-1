def calculate_margin(revenue, cost):
    return (revenue - cost) / revenue if revenue else 0

def get_metrics_definition():
    return {
        "margin": " (revenue - cost) / revenue ",
        "revenue": "sum of revenue",
        "cost": "sum of cost"
    }
# revenue=sum()
# cost=sum()