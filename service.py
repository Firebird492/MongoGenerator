
class Field:
    def __init__(self, json: dict) -> None:
        self.name = json["name"]
        self.isRequired = json.get("isRequired", False)


class Table:
    def __init__(self, json: dict) -> None:
        self.name = json["name"]
        self.noDelete = json.get("noDelete", False)
        self.fields = []
        for f in json["fields"]:
            self.fields.append(Field(f))

    def getName(self):
        return self.name
    
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

