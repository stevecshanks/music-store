from store import create_app
from rq import Connection, Worker
from store.services import DownloadQueueFactory

app = create_app()
app.app_context().push()

with Connection(DownloadQueueFactory.create()):
    worker = Worker(app.config['REDIS_QUEUES'])
    worker.work()
