import asyncio
import notify2
import os
import schedule
import time
import random
from datetime import datetime
from todoist_api_python.api_async import TodoistAPIAsync

def show_notification(title: str, content: str):
    icon = "file://" + os.path.join(os.path.dirname(os.path.abspath(__file__)), "notification.png")
    n = notify2.Notification(title, content, icon)
    n.set_urgency(notify2.URGENCY_NORMAL)
    n.show()

async def main():
    notify2.init("My Application")
    
    api = TodoistAPIAsync(os.getenv("TODOIST_API_TOKEN", ""))
    
    inbox = None
    projects_gen = await api.get_projects()
    async for page in projects_gen:
        for project in page:
            if project.is_inbox_project:
                inbox = project
                break
        if inbox:
            break
    if not inbox:
        raise SystemExit("Could not find the Todoist Inbox project")
    
    tasks = []
    async for page in await api.get_tasks(project_id=inbox.id):
        for task in page:
            if task.parent_id is None:
                tasks.append(task.content)
                
    if not tasks:
        print("No tasks found in Inbox")
        return

    times = [
            ("05:00"),
            ("05:30"),
            ("06:00"),
            ("06:30"),
            ("07:00"),
            ("07:30"),
            ("08:00"),
            ("08:30"),
            ("09:00"),
            ("09:30"),
            ("10:00"),
            ("10:30"),
            ("11:00"),
            ("11:30"),
            ("12:00"),
            ("12:30"),
            ("13:00"),
            ("13:30"),
            ("14:00"),
            ("14:30"),
            ("15:00"),
            ("15:30"),
            ("16:00"),
            ("16:30"),
            ("17:00"),
            ("17:30"),
            ("18:00"),
            ("18:30"),
            ("19:00"),
            ("19:30"),
            ("20:00"),
            ("20:30"),
            ("21:00"),
            ("21:30"),
    ]

    now = datetime.now()
    most_recent_past = None  
    for time in times:
        scheduled = datetime.strptime(time, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
        if scheduled <= now:
            if most_recent_past is None or scheduled > most_recent_past:
                most_recent_past = scheduled
        else:
            schedule.every().day.at(time).do(
                lambda t=time: show_notification("Inbox", random.choice(tasks))
            )
    if most_recent_past is not None:
        show_notification("Inbox", random.choice(tasks))

    while True:
        schedule.run_pending()
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
