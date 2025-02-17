import sqlalchemy
import datetime

from sqlalchemy import Column, String, BigInteger, Integer, DateTime, ForeignKey, Sequence, Table, Boolean, Float, Date
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

BaseModel = declarative_base()

def UUIDColumn(name=None):
    if name is None:
        return Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
    else:
        return Column(name, UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("gen_random_uuid()"), unique=True)
    
#id = Column(UUID(as_uuid=True), primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"),)

###########################################################################################################################
#
# zde definujte sve SQLAlchemy modely
# je-li treba, muzete definovat modely obsahujici jen id polozku, na ktere se budete odkazovat
#
    
class ProjectModel(BaseModel):
    """Spravuje data spojena s projekty"""
    __tablename__ = 'projects'
    
    id = UUIDColumn()
    valid = Column(Boolean)
    name = Column(String)
    startDate = Column(Date)
    endDate = Column(Date)
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())

    projectType_id = Column(ForeignKey('projectProjectTypes.id'), primary_key=True)                      
    projectType = relationship('ProjectTypeModel', back_populates='projects') 

    finance = relationship('FinanceModel', back_populates='project') #
    milestones = relationship('MilestoneModel', back_populates='project') #                     

    group_id = Column(ForeignKey('groups.id'), primary_key=True)
    group = relationship('GroupModel')

class ProjectTypeModel(BaseModel):
    """Spravuje data spojena s typy projektu"""
    __tablename__ = 'projectProjectTypes'
    
    id = UUIDColumn()
    name = Column(String)
                            
    projects = relationship('ProjectModel', back_populates='projectType')                     
    
class FinanceModel(BaseModel):
    """Spravuje data spojena s financemi projektu"""
    __tablename__ = 'projectFinances'
    
    id = UUIDColumn()
    name = Column(String)
    amount = Column(Float)
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
        
    project_id = Column(ForeignKey('projects.id'), primary_key=True)
    project = relationship('ProjectModel')              
                            
    financeType_id = Column(ForeignKey('projectFinanceTypes.id'), primary_key=True)
    financeType = relationship('FinanceTypeModel', back_populates='finances')
                               
class FinanceTypeModel(BaseModel):
    """Spravuje data spojena s typy financi projektu"""
    __tablename__ = 'projectFinanceTypes'
    
    id = UUIDColumn()
    name = Column(String)
   
    finances = relationship('FinanceModel', back_populates='financeType')
      
class MilestoneModel(BaseModel):
    """Spravuje data spojena s milniky projektu"""
    __tablename__ = 'projectMilestones'
    
    id = UUIDColumn()
    name = Column(String)                          
    date = Column(Date)
    lastchange = Column(DateTime, server_default=sqlalchemy.sql.func.now())
    
    project_id = Column(ForeignKey('projects.id'), primary_key=True)
    project = relationship('ProjectModel')

class GroupModel(BaseModel):
    """Spravuje data spojena se skupinou zpracovavajici projekt"""
    __tablename__ = 'groups'
    
    id = UUIDColumn()
    
###########################################################################################################################

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine

async def startEngine(connectionstring, makeDrop=False, makeUp=True):
    """Provede nezbytne ukony a vrati asynchronni SessionMaker """
    asyncEngine = create_async_engine(connectionstring) 

    async with asyncEngine.begin() as conn:
        if makeDrop:
            await conn.run_sync(BaseModel.metadata.drop_all)
            print('BaseModel.metadata.drop_all finished')
        if makeUp:
            await conn.run_sync(BaseModel.metadata.create_all)    
            print('BaseModel.metadata.create_all finished')

    async_sessionMaker = sessionmaker(
        asyncEngine, expire_on_commit=False, class_=AsyncSession
    )
    return async_sessionMaker

import os
def ComposeConnectionString():
    """Odvozuje connectionString z promennych prostredi (nebo z Docker Envs, coz je fakticky totez).
       Lze predelat na napr. konfiguracni file.
    """
    user = os.environ.get("POSTGRES_USER", "postgres")
    password = os.environ.get("POSTGRES_PASSWORD", "example")
    database =  os.environ.get("POSTGRES_DB", "data")
    hostWithPort =  os.environ.get("POSTGRES_HOST", "postgres:5432")
    
    driver = "postgresql+asyncpg" #"postgresql+psycopg2"
    connectionstring = f"{driver}://{user}:{password}@{hostWithPort}/{database}"

    return connectionstring