from sinapse.celeryconfig import app
from sinapse.detran.client import get_person_photo
from sinapse.images import get_vehicle_photo


@app.task
def get_person_photo_asynch(node_id):
    get_person_photo(node_id)


@app.task
def get_vehicle_photo_asynch(node_id):
    get_vehicle_photo(node_id)
