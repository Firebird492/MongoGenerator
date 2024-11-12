
class Field:
    def __init__(self, json: dict) -> None:
        self.name = json["name"]
        self.isRequired = json.get("isRequired", False)
        self.type = json["type"]

        defaults = {
            "str": "",
            "int": -1,
            "float": -1,
            "array": "[]",
            "bool": False,
        }
        self.default = json.get("default", defaults[self.type] )
        self.example = json.get("example", None)

    def getName(self):
        return self.name
    
    def getDefault(self):
        if self.type == "str" and self.default != "null":
            return f'"{self.default}"'
        if self.type == "bool":
            if self.default == True:
                return "true"
            else:
                return "false"
        return self.default
    
    def getExample(self, seed: int):
        if self.example:
            return self.example[seed%3]
        if self.type == "int":
            return seed
        if self.type == "str":
            return f'"example{str(seed)}"'
        if self.type == "float":
            return seed * 1.2
        if self.type == "array":
            ar = []
            for i in range(3):
                ar.append(f"arrayVal{str(seed+i)}")
            return ar
        if self.type == "bool":
            if seed % 2:
                return True
            return False
        raise Exception("Not valid Type")



class Table:
    def __init__(self, json: dict) -> None:
        self.name = json["name"]

        if "plural" not in self.name:
            self.name["plural"] = self.name["name"] + "s"

        self.noDelete = json.get("noDelete", False)
        self.fields = []
        for f in json["fields"]:
            self.fields.append(Field(f))

    def getName(self):
        return self.name["name"]
    
    def getPluralName(self):
        return self.name["plural"]
    
    def getFields(self):
        return self.fields
    
    def excludeDelete(self):
        return self.noDelete
    
    def getRequiredFields(self):
        return [f for f in self.fields if f.isRequired]



class Service:
    def __init__(self, json: dict) -> None:
        self.tables = []
        for t in json["tables"]:
            self.tables.append(Table(t))

    def getTables(self):
        return self.tables

