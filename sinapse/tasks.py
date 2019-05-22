from sinapse.celeryconfig import app
from sinapse.detran.client import get_person_photo
from sinapse.images import get_vehicle_photo


@app.task
def get_person_photo_asynch(infos):
    get_person_photo(infos, label='Pessoa')


@app.task
def get_vehicle_photo_asynch(infos):
    get_vehicle_photo(infos, label='Veiculo')
