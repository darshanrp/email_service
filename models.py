from datetime import datetime
from database import Base 
from sqlalchemy import Column, String, Integer, create_engine, Text, DateTime


class Email(Base):
	__tablename__ = "email"

	id = Column(Integer, primary_key=True)
	from_email = Column(String(1024))
	from_name = Column(String(1024))
	to_email = Column(String(1024))
	to_name = Column(String(1024))
	subject = Column(String(2048))
	body = Column(Text)
	send_at = Column(DateTime)
	created_at = Column(DateTime, default=datetime.utcnow())
	
	def __repr__(self):
		return '<Email %r>' % self.id
