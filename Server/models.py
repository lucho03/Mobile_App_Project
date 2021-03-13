from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "User"

    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    login_id = Column(String(36), nullable=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    @property
    def is_authenticated(self):
        return self.login_id

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.login_id

    report = relationship("Report", back_populates="user",
                          cascade="all, delete", passive_deletes=True)


class Company(Base):
    __tablename__ = "Company"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    email = Column(String(80), unique=True, nullable=False)


class Report(Base):
    __tablename__ = "Report"

    id = Column(Integer, primary_key=True)
    photo = Column(String(80), nullable=False)
    description = Column(String(100), nullable=True)
    location = Column(String(80), nullable=False)
    confirm_trash = Column(Enum('trash','non_trash'), nullable=False)
    trash = Column(String(200), nullable=True)

    user_id = Column(Integer, ForeignKey('User.id', ondelete="CASCADE"))
    user = relationship("User", back_populates="report")
