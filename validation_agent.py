class ValidationAgent:
    def validate(self, sql):
        if "DROP" in sql or "DELETE" in sql:
            return False
        return True