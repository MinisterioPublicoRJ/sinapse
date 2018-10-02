from sinapse.detran.celeryconfig import app
from sinapse.detran.client import get_photos


@app.task
def get_photos_asynch(node_id):
    get_photos(node_id)
