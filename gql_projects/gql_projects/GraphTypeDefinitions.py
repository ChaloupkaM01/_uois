from typing import List, Union, Optional
import typing
from unittest import result
import strawberry as strawberryA
import datetime
import uuid

from contextlib import asynccontextmanager

@asynccontextmanager
async def withInfo(info):
    asyncSessionMaker = info.context['asyncSessionMaker']
    async with asyncSessionMaker() as session:
        try:
            yield session
        finally:
            pass

def AsyncSessionFromInfo(info):
    print('obsolete function used AsyncSessionFromInfo, use withInfo context manager instead')
    return info.context['session']

def AsyncSessionMakerFromInfo(info):
    return info.context['asyncSessionMaker']

###########################################################################################################################
#
# zde definujte sve GQL modely
# - nove, kde mate zodpovednost
# - rozsirene, ktere existuji nekde jinde a vy jim pridavate dalsi atributy
#
###########################################################################################################################

#GQL PROJECT
from gql_projects.GraphResolvers import resolveProjectById, resolveProjectAll, resolveUpdateProject, resolveInsertProject
@strawberryA.federation.type(keys=["id"],description="""Entity representing a project""")
class ProjectGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveProjectById(session, id)
            result._type_definition = cls._type_definition # little hack :)
            return result
    
    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""If project is valid or not""")
    def valid(self) -> bool:
        return self.valid

    @strawberryA.field(description="""Start date""")
    def startDate(self) -> datetime.date:
        return self.startDate

    @strawberryA.field(description="""End date""")
    def endDate(self) -> datetime.date:
        return self.endDate

    @strawberryA.field(description="""Last change""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Project type of project""")
    async def projectType(self, info: strawberryA.types.Info) -> 'ProjectTypeGQLModel':
        async with withInfo(info) as session:
            result = await resolveProjectTypeById(session, self.projectType_id)
            return result

    @strawberryA.field(description="""List of finances, related to a project""")
    async def finances(self, info: strawberryA.types.Info) -> typing.List['FinanceGQLModel']:
        async with withInfo(info) as session:
            result = await resolveFinancesForProject(session, self.id)
            return result

    @strawberryA.field(description="""List of milestones, related to a project""")
    async def milestones(self, info: strawberryA.types.Info) -> typing.List['MilestoneGQLModel']:
        async with withInfo(info) as session:
            result = await resolveMilestonesForProject(session, self.id)
            return result

    @strawberryA.field(description="""Group, related to a project""")
    async def group(self) -> 'GroupGQLModel':
        return GroupGQLModel(id=self.group_id)

    @strawberryA.field(description="""Returns the project editor""")
    async def editor(self, info: strawberryA.types.Info) -> Union['ProjectEditorGQLModel', None]:
        return self
    

 #GQL PROJECT UPDATE
@strawberryA.input(description="""Entity representing a project update""")
class ProjectUpdateGQLModel:
    lastchange: datetime.datetime
    name:  Optional[str] = None
    valid: Optional[bool] = None
    start_date: Optional[datetime.date] = None 
    end_date: Optional[datetime.date] = None 
    project_type_id: Optional[uuid.UUID] = None
    group_id: Optional[uuid.UUID] = None


#GQL PROJECT EDITOR
from gql_projects.GraphResolvers import resolveRemoveFinance, resolveRemoveMilestone
@strawberryA.federation.type(keys=["id"], description="""Entity representing an editable project""")
class ProjectEditorGQLModel:
    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveProjectById(session, id)
            result._type_definition = cls._type_definition # little hack :)
            return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result status of update operation""")
    def result(self) -> str:
        return self.result 

    @strawberryA.field(description="""Result of update operation""")
    async def project(self, info: strawberryA.types.Info) -> ProjectGQLModel:
        async with withInfo(info) as session:
            result = await resolveProjectById(session, id)
            return result

    @strawberryA.field(description="""Updates the project data""")
    async def update(self, info: strawberryA.types.Info, data: ProjectUpdateGQLModel) -> 'ProjectEditorGQLModel':
        lastchange = data.lastchange
        async with withInfo(info) as session:
            await resolveUpdateProject(session, id=self.id, data=data)
            if lastchange == data.lastchange:
                # no change
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = ProjectEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result    

    @strawberryA.field(description="""Invalidate project""")
    async def invalidate_project(self, info: strawberryA.types.Info) -> 'ProjectGQLModel':
        async with withInfo(info) as session:
            project = await resolveProjectById(session, self.id)
            project.valid = False
            await session.commit()
            return project
        
    @strawberryA.field(description="""Create new finance""")
    async def add_finance(self, info: strawberryA.types.Info, name: str, amount: int, financeType_id: uuid.UUID) -> 'FinanceGQLModel':
        async with withInfo(info) as session:
            result = await resolveInsertFinance(session, None, extraAttributes={'name': name, 'amount': amount, 'financeType_id': financeType_id, 'project_id': self.id})
            return result    

    @strawberryA.field(description="""Remove finance""")
    async def remove_finance(self, info: strawberryA.types.Info, finance_id: uuid.UUID) -> str:
        async with withInfo(info) as session:
            result = await resolveRemoveFinance(session, self.id, finance_id)
            return result
        
    @strawberryA.field(description="""Create new milestone""")
    async def add_milestone(self, info: strawberryA.types.Info, name: str, date: datetime.date) -> 'MilestoneGQLModel':
        async with withInfo(info) as session:
            result = await resolveInsertMilestone(session, None, extraAttributes={'name': name, 'date': date, 'project_id': self.id})
            return result  

    @strawberryA.field(description="""Remove milestone""")
    async def remove_milestone(self, info: strawberryA.types.Info, milestone_id: uuid.UUID) -> str:
        async with withInfo(info) as session:
            result = await resolveRemoveMilestone(session, self.id, milestone_id)
            return result
    

#GQL PROJECT TYPE
from gql_projects.GraphResolvers import resolveProjectTypeById, resolveProjectTypeAll, resolveProjectsForProjectType, resolveFinancesForProject, resolveMilestonesForProject
@strawberryA.federation.type(keys=["id"],description="""Entity representing a project types""")
class ProjectTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveProjectTypeById(session, id)
            result._type_definition = cls._type_definition # little hack :)
            return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name
    
    @strawberryA.field(description="""List of projects, related to project type""")
    async def projects(self, info: strawberryA.types.Info) -> typing.List['ProjectGQLModel']:
        async with withInfo(info) as session:
            result = await resolveProjectsForProjectType(session, self.id)
            return result


#GQL FINANCE
from gql_projects.GraphResolvers import resolveFinanceById, resolveFinanceAll, resolveInsertFinance
@strawberryA.federation.type(keys=["id"],description="""Entity representing a finance""")
class FinanceGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveFinanceById(session, id)
            result._type_definition = cls._type_definition # little hack :)
            return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Amount""")
    def amount(self) -> float:
        return self.amount

    @strawberryA.field(description="""Last change""")
    def lastchange(self) -> datetime.datetime:
        return self.lastchange

    @strawberryA.field(description="""Project of finance""")
    async def project(self, info: strawberryA.types.Info) -> 'ProjectGQLModel':
        async with withInfo(info) as session:
            result = await resolveProjectById(session, self.project_id)
            return result

    @strawberryA.field(description="""Finance type of finance""")
    async def financeType(self, info: strawberryA.types.Info) -> 'FinanceTypeGQLModel':
        async with withInfo(info) as session:
            result = await resolveFinanceTypeById(session, self.financeType_id)
            return result
        
    @strawberryA.field(description="""Returns the finance editor""")
    async def editor(self, info: strawberryA.types.Info) -> Union['FinanceEditorGQLModel', None]:
        return self


 #GQL FINANCE UPDATE
@strawberryA.input(description="""Entity representing a finance update""")
class FinanceUpdateGQLModel:
    lastchange: datetime.datetime
    name:  Optional[str] = None
    amount: Optional[int] = None
    finance_type_id: Optional[uuid.UUID] = None


#GQL FINANCE EDITOR
from gql_projects.GraphResolvers import resolveUpdateFinance
@strawberryA.federation.type(keys=["id"], description="""Entity representing an editable finance""")
class FinanceEditorGQLModel:
    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveFinanceById(session, id)
            result._type_definition = cls._type_definition # little hack :)
            return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result status of update operation""")
    def result(self) -> str:
        return self.result 

    @strawberryA.field(description="""Result of update operation""")
    async def finance(self, info: strawberryA.types.Info) -> FinanceGQLModel:
        async with withInfo(info) as session:
            result = await resolveFinanceById(session, id)
            return result

    @strawberryA.field(description="""Updates the finance data""")
    async def update(self, info: strawberryA.types.Info, data: FinanceUpdateGQLModel) -> 'FinanceEditorGQLModel':
        lastchange = data.lastchange
        async with withInfo(info) as session:
            await resolveUpdateFinance(session, id=self.id, data=data)
            if lastchange == data.lastchange:
                # no change
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = FinanceEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result


#GQL FINANCE TYPE
from gql_projects.GraphResolvers import resolveFinanceTypeById, resolveFinanceTypeAll, resolveFinancesForFinanceType
@strawberryA.federation.type(keys=["id"],description="""Entity representing a finance type""")
class FinanceTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveFinanceTypeById(session, id)
            result._type_definition = cls._type_definition # little hack :)
            return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name
    
    @strawberryA.field(description="""List of finances, related to finance type""")
    async def finances(self, info: strawberryA.types.Info) -> typing.List['FinanceGQLModel']:
        async with withInfo(info) as session:
            result = await resolveFinancesForFinanceType(session, self.id)
            return result


#GQL MILESTONE
from gql_projects.GraphResolvers import resolveMilestoneById, resolveMilestoneAll, resolveInsertMilestone
@strawberryA.federation.type(keys=["id"],description="""Entity representing a milestone""")
class MilestoneGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveMilestoneById(session, id)
            result._type_definition = cls._type_definition # little hack :)
            return result

    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name

    @strawberryA.field(description="""Date""")
    def date(self) -> datetime.date:
        return self.date

    @strawberryA.field(description="""Last change""")
    def lastChange(self) -> datetime.datetime:
        return self.lastChange

    @strawberryA.field(description="""Project of milestone""")
    async def project(self, info: strawberryA.types.Info) -> 'ProjectGQLModel':
        async with withInfo(info) as session:
            result = await resolveProjectById(session, self.project_id)
            return result
    
    @strawberryA.field(description="""Returns the milestone editor""")
    async def editor(self, info: strawberryA.types.Info) -> Union['MilestoneEditorGQLModel', None]:
        return self
        

 #GQL MILESTONE UPDATE
@strawberryA.input(description="""Entity representing a milestone update""")
class MilestoneUpdateGQLModel:
    lastchange: datetime.datetime
    name:  Optional[str] = None
    date: Optional[datetime.date] = None


#GQL MILESTONE EDITOR
from gql_projects.GraphResolvers import resolveUpdateMilestone
@strawberryA.federation.type(keys=["id"], description="""Entity representing an editable milestone""")
class MilestoneEditorGQLModel:
    id: strawberryA.ID = None
    result: str = None

    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        async with withInfo(info) as session:
            result = await resolveMilestoneById(session, id)
            result._type_definition = cls._type_definition # little hack :)
            return result

    @strawberryA.field(description="""Entity primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Result status of update operation""")
    def result(self) -> str:
        return self.result 

    @strawberryA.field(description="""Result of update operation""")
    async def milestone(self, info: strawberryA.types.Info) -> MilestoneGQLModel:
        async with withInfo(info) as session:
            result = await resolveMilestoneById(session, id)
            return result

    @strawberryA.field(description="""Updates the milestone data""")
    async def update(self, info: strawberryA.types.Info, data: MilestoneUpdateGQLModel) -> 'MilestoneEditorGQLModel':
        lastchange = data.lastchange
        async with withInfo(info) as session:
            await resolveUpdateMilestone(session, id=self.id, data=data)
            if lastchange == data.lastchange:
                # no change
                resultMsg = "fail"
            else:
                resultMsg = "ok"
            result = MilestoneEditorGQLModel()
            result.id = self.id
            result.result = resultMsg
            return result


#GQL GROUP
from gql_projects.GraphResolvers import resolveProjectsForGroup
@strawberryA.federation.type(extend=True, keys=["id"],description="""Entity representing a group""")
class GroupGQLModel:
    id: strawberryA.ID = strawberryA.federation.field(external=True)
    @classmethod
    def resolve_reference(cls, id: strawberryA.ID):
        return GroupGQLModel(id=id)

    @strawberryA.field(description="""List of projects, related to group""")
    async def projects(self, info: strawberryA.types.Info) -> typing.List['ProjectGQLModel']:
        async with withInfo(info) as session:
            result = await resolveProjectsForGroup(session, self.id)
            return result

###########################################################################################################################
#
# zde definujte svuj Query model
#
###########################################################################################################################

from gql_projects.DBFeeder import randomDataStructure

@strawberryA.type(description="""Type for query root""")
class Query:  
    @strawberryA.field(description="""Returns a list of projects""")
    async def project_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[ProjectGQLModel]:
        async with withInfo(info) as session:
            result = await resolveProjectAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Returns project by its id""")
    async def project_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[ProjectGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolveProjectById(session, id)
            return result

    @strawberryA.field(description="""Returns a list of project types""")
    async def project_type_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[ProjectTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveProjectTypeAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Returns a list of finances""")
    async def finance_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[FinanceGQLModel]:
        async with withInfo(info) as session:
            result = await resolveFinanceAll(session, skip, limit)
            return result
    
    @strawberryA.field(description="""Returns finance by its id""")
    async def finance_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[FinanceGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolveFinanceById(session, id)
            return result

    @strawberryA.field(description="""Returns a list of finance types""")
    async def finance_type_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[FinanceTypeGQLModel]:
        async with withInfo(info) as session:
            result = await resolveFinanceTypeAll(session, skip, limit)
            return result

    @strawberryA.field(description="""Returns a list of milestones""")
    async def milestone_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[MilestoneGQLModel]:
        async with withInfo(info) as session:
            result = await resolveMilestoneAll(session, skip, limit)
            return result
    
    @strawberryA.field(description="""Returns milestone by its id""")
    async def milestone_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[MilestoneGQLModel, None]:
        async with withInfo(info) as session:
            result = await resolveMilestoneById(session, id)
            return result

    @strawberryA.field(description="""Returns a list of projects for group""")
    async def project_by_group(self, info: strawberryA.types.Info, id: strawberryA.ID) -> List[ProjectGQLModel]:
        async with withInfo(info) as session:
            result = await resolveProjectsForGroup(session, id)
            return result
    
    @strawberryA.field(description="""Random project""")
    async def randomProject(self, info: strawberryA.types.Info) -> ProjectGQLModel:
        async with withInfo(info) as session:
            firstNewID = await randomDataStructure(session)
            result = await resolveProjectById(session, firstNewID)
            return result