from models.base_model import BaseModel
from models import storage
from models.engine.file_storage import FileStorage
from models.state import State

storage.reload()
obj_dict = storage.all(State)
print(obj_dict)

id_ = 'State.8e269357-e81a-4ade-b220-2442609e0738'
print(obj_dict[id_].id)

print(storage.get(State, obj_dict[id_].id).to_dict())
