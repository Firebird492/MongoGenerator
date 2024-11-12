from jinja2 import Environment, FileSystemLoader
from service import Service
import json
import os



path = './renders'
if not os.path.exists(path):
    os.makedirs(path)

with open('inputs/tmc.json', 'r') as file:
    jsonData = json.load(file)

service = Service(jsonData)
env = Environment(loader = FileSystemLoader('templates'))
# mongo functions
template = env.get_template('MongoFunctionsTemplate.jinja')
output = template.render(Service = service)
with open("renders/outputFileName.js", 'w') as f:
    print(output, file = f)

# models
template = env.get_template('MongoModelsTemplate.jinja')
output = template.render(Service = service)
with open("renders/models.js", 'w') as f:
    print(output, file = f)