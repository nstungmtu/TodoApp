import hashlib
from models.model_base import ModelBase
from models.todo import Todo
from models.tag import Tag
from models.todo_tag import TodoTag
from models.user import User
from sqlalchemy.orm import Session


def ini_db(engine):
    with engine.begin() as conn:
        #Xóa tất cả các bảng cũ và tạo lại các bảng mới
        ModelBase.metadata.drop_all(engine)
        ModelBase.metadata.create_all(engine)
        #thêm lại tài khoản admin
        session = Session(bind=conn)
        admin_user = User(login="admin", email="admin@example.com", is_admin=True, name="Administrator")
        admin_user.password = hashlib.sha256("admin".encode("utf-8")).hexdigest()
        session.add(admin_user)
        session.commit()
        #Thêm dữ liệu mẫu
        user1 = User(login="john", email="john@example.com", name="John Doe")
        user1.password = hashlib.sha256("password".encode("utf-8")).hexdigest()
        user2 = User(login="jane", email="jane@example.com", name="Jane Smith")
        user2.password = hashlib.sha256("password".encode("utf-8")).hexdigest()
        session.add_all([user1, user2])
        session.commit()
        tag1 = Tag(name="Work")
        tag2 = Tag(name="Personal")
        tag3 = Tag(name="School")
        session.add_all([tag1, tag2, tag3])
        session.commit()
        todo1 = Todo(title="Finish project report", description="Complete the final report for the project", user=user1)
        todo2 = Todo(title="Buy groceries", description="Buy milk, eggs, and bread", user=user1)
        todo3 = Todo(title="Meeting with team", description="Discuss project progress with team members", user=user2)
        session.add_all([todo1, todo2, todo3])
        session.commit()
        todo1.tags.append(TodoTag(tag=tag1, todo=todo1))
        todo1.tags.append(TodoTag(tag=tag2, todo=todo1))
        todo2.tags.append(TodoTag(tag=tag2, todo=todo2))
        todo2.tags.append(TodoTag(tag=tag3, todo=todo2))
        todo3.tags.append(TodoTag(tag=tag1, todo=todo3))
        session.commit()
        session.close()
        print("Database initialized successfully.")

