
class Field:
    def __init__(self, json: dict) -> None:
        self.name = json["name"]
        self.isRequired = json.get("isRequired", False)
        self.type = json.get("type", "NA")

        defaults = {
            "str": "''",
            "int": -1,
            "float": -1,
            "array": "[]",
            "bool": "false",
            "NA": "null",
        }
        self.default = defaults[self.type] 

    def getName(self):
        return self.name
    
    def getDefault(self):
        return self.default



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

