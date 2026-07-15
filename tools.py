#for simple testing taking simple metrics and simple data
def get_metric(metric):
    if metric == "margin":
      return "Margin = (Revenue - Cost)/Revenue"
    return "MEtric not found"

def sample_data():
   return{
      "Germany":{"Q3": 0.20, "Q4": 0.13},
      "Russia":{"Q3": 0.30, "Q4": 0.51}
   }
