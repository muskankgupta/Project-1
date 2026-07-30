import yaml

class SemanticLayer:
    def __init__(self, file_path):
        with open(file_path, "r") as f:
            self.schema = yaml.safe_load(f)

        self.metrics = {m["name"]: m for m in self.schema["metrics"]}
        self.dimensions = {d["name"]: d for d in self.schema["dimensions"]}
        self.aliases = self.schema.get("semantic_aliases", {})

    def get_metric(self, name):
        return self.metrics.get(name)

    def resolve_alias(self, word):
        for key, values in self.aliases.items():
            if word.lower() in values:
                return key
        return word