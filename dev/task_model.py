from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    is_completed = Column(Boolean, default=False)

class Task_model:
    def __init__(self, db_url='sqlite:///tasks.db'):
        self.engine = create_engine(db_url, echo=True)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def add_task(self, task_json):
        task = Task(title=task_json["title"], is_completed=task_json.get("is_completed", False))
        with self.Session() as session:
            session.add(task)
            session.commit()
            return task.id

    def get_all_task(self):
        with self.Session() as session:
            tasks = session.query(Task).all()
            return {"tasks": [{"id": task.id, "title": task.title, "is_completed": task.is_completed} for task in tasks]}

    def get_task(self, task_id):
        with self.Session() as session:
            task = session.query(Task).filter(Task.id == task_id).first()
            if task:
                return {"id": task.id, "title": task.title, "is_completed": task.is_completed}, 200
            return {"error": "There is no task at that id"}, 404

    def update_task(self, task_id, new_data):
        with self.Session() as session:
            task = session.query(Task).filter(Task.id == task_id).first()
            if task:
                task.title = new_data.get("title", task.title)
                task.is_completed = new_data.get("is_completed", task.is_completed)
                session.commit()
                return None, 204
            return {"error": "There is no task at that id"}, 404

    def delete_task(self, task_id):
        with self.Session() as session:
            task = session.query(Task).filter(Task.id == task_id).first()
            if task:
                session.delete(task)
                session.commit()
                return None, 204
            return {"error": "There is no task at that id"}, 404
