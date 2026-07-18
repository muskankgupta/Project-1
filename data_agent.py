class DataAgent:
    def __init__(self, data):
        self.data = data

    def run(self ,metric):
       if metric in self.data:
            return {
                "status": "success",
                "metric": metric,
                "value" : self.data[metric]
            }
       return {
            "status": "error"}