from backend.db.models import SkyTechScriptsLogs
from datetime import datetime
from sqlalchemy.orm import Session
from backend.db.models import engine
import pytz

def add_log(task_id:str, task_name: str, task_response: str, task_execution_time: float | None, task_error_message:str | None) -> None:
    with Session(engine) as session:
        log = SkyTechScriptsLogs(task_id=task_id, task_name=task_name, task_response=task_response,
                                 task_execution_time=task_execution_time, task_error_message=task_error_message,
                                 log_time=datetime.now(pytz.timezone('Europe/Berlin')))
        session.add(log)
        session.commit()
