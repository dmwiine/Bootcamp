from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///dojo.db', echo=True)
Base = declarative_base()


class Fellow(Base):
    """"""
    __tablename__ = "fellow"

    fellow_id = Column(Integer, primary_key=True)
    living_space_id = Column('living_space_id', Integer, ForeignKey("living_space.living_space_id"), nullable=True)
    office_id = Column('office_id', Integer, ForeignKey("office.office_id"), nullable=True)
    name = Column(String)

    fellow_living_space = relationship("living_space", foreign_keys=[living_space_id])
    fellow_office = relationship("office",foreign_keys=[office_id])
    # ----------------------------------------------------------------------
    def __init__(self, fellow_id, living_space_id, office_id, name):
        """"""
        self.fellow_id = fellow_id
        self.living_space_id = living_space_id
        self.office_id = office_id
        self.name = name


class LivingSpace(Base):
    """"""
    __tablename__ = "living_space"

    living_space_id = Column(Integer, primary_key=True)
    name = Column(String)
    spaces_available = Column(Integer)

    # ----------------------------------------------------------------------
    def __init__(self, living_space_id, name, spaces_available):
        """"""
        self.living_space_id = living_space_id
        self.name = name
        self.spaces_available = spaces_available


class Office(Base):
    """"""
    __tablename__ = "office"

    office_id = Column(Integer, primary_key=True)
    name = Column(String)
    spaces_available = Column(Integer)

    # ----------------------------------------------------------------------
    def __init__(self, office_id, name, spaces_available):
        """"""
        self.office_id = office_id
        self.name = name
        self.spaces_available = spaces_available




class Staff(Base):
    """"""
    __tablename__ = "staff"

    staff_id = Column(Integer, primary_key=True)
    office_id = Column('office_id', Integer, ForeignKey("office.office_id"), nullable=True)
    name = Column(String)

    staff_office = relationship("office", foreign_keys=[office_id])
    # ----------------------------------------------------------------------
    def __init__(self, staff_id, office_id, name):
        """"""
        self.staff_id = staff_id
        self.office_id = office_id
        self.name = name


Base.metadata.create_all(engine)