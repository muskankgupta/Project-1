class SemanticMapper:
    def __init__(self, semantic_layer):
        self.semantic = semantic_layer

    def map_query(self, user_query):
        query = user_query.lower()

        metric = None
        for m in self.semantic.metrics:
            if m in query:
                metric = m

        # alias support
        for word in query.split():
            resolved = self.semantic.resolve_alias(word)
            if resolved in self.semantic.metrics:
                metric = resolved

        dimensions = []
        for dim in self.semantic.dimensions:
            if dim in query:
                dimensions.append(dim)

        return {
            "metric": metric or "total_revenue",
            "dimensions": dimensions
        }