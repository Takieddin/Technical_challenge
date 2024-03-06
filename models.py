from sqlalchemy import create_engine, Column, Integer, Float, LargeBinary, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "sqlite:///./test.db"  # Adjust as needed for your database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    image_data = Column(LargeBinary)  # Storing compressed and resized image as binary
    depths = relationship("Depth", back_populates="image")
    name = Column(String)

class Depth(Base):
    __tablename__ = "depths"
    id = Column(Integer, primary_key=True, index=True)
    value = Column(Integer, index=True)
    raw_number = Column(Integer, index=True)  # New column for the CSV index
    image_id = Column(Integer, ForeignKey('images.id'))
    image = relationship("Image", back_populates="depths")

# Create the database tables
Base.metadata.create_all(bind=engine)

