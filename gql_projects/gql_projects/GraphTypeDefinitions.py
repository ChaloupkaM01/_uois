from typing import List, Union
import typing
from unittest import result
import strawberry as strawberryA
import datetime
import uuid

def AsyncSessionFromInfo(info):
    return info.context['session']

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
        result = await resolveProjectById(AsyncSessionFromInfo(info), id)
        result._type_definition = cls._type_definition # little hack :)
        return result
    
    @strawberryA.field(description="""Primary key""")
    def id(self) -> strawberryA.ID:
        return self.id

    @strawberryA.field(description="""Name""")
    def name(self) -> str:
        return self.name

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
        result = await resolveProjectTypeById(AsyncSessionFromInfo(info), self.projectType_id)
        return result

    @strawberryA.field(description="""List of finances, related to a project""")
    async def finances(self, info: strawberryA.types.Info) -> typing.List['FinanceGQLModel']:
        result = await resolveFinancesForProject(AsyncSessionFromInfo(info), self.id)
        return result

    @strawberryA.field(description="""List of milestones, related to a project""")
    async def milestones(self, info: strawberryA.types.Info) -> typing.List['MilestoneGQLModel']:
        result = await resolveMilestonesForProject(AsyncSessionFromInfo(info), self.id)
        return result

    @strawberryA.field(description="""Group, related to a project""")
    async def group(self, info: strawberryA.types.Info) -> 'GroupGQLModel':
        return GroupGQLModel(id=self.group_id)


#GQL PROJECT TYPE
from gql_projects.GraphResolvers import resolveProjectTypeById, resolveProjectTypeAll, resolveUpdateProjectType, resolveInsertProjectType, resolveProjectsForProjectType, resolveFinancesForProject, resolveMilestonesForProject
@strawberryA.federation.type(keys=["id"],description="""Entity representing a project types""")
class ProjectTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveProjectTypeById(AsyncSessionFromInfo(info), id)
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
        result = await resolveProjectsForProjectType(AsyncSessionFromInfo(info), self.id)
        return result


#GQL FINANCE
from gql_projects.GraphResolvers import resolveFinanceById, resolveFinanceAll, resolveUpdateFinance, resolveInsertFinance
@strawberryA.federation.type(keys=["id"],description="""Entity representing a finance""")
class FinanceGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveFinanceById(AsyncSessionFromInfo(info), id)
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
        result = await resolveProjectById(AsyncSessionFromInfo(info), self.project_id)
        return result

    @strawberryA.field(description="""Finance type of finance""")
    async def financeType(self, info: strawberryA.types.Info) -> 'FinanceTypeGQLModel':
        result = await resolveFinanceTypeById(AsyncSessionFromInfo(info), self.financeType_id)
        return result


#GQL FINANCE TYPE
from gql_projects.GraphResolvers import resolveFinanceTypeById, resolveFinanceTypeAll, resolveUpdateFinanceType, resolveInsertFinanceType, resolveFinancesForFinanceType
@strawberryA.federation.type(keys=["id"],description="""Entity representing a finance type""")
class FinanceTypeGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveFinanceTypeById(AsyncSessionFromInfo(info), id)
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
        result = await resolveFinancesForFinanceType(AsyncSessionFromInfo(info), self.id)
        return result


#GQL MILESTONE
from gql_projects.GraphResolvers import resolveMilestoneById, resolveMilestoneAll, resolveUpdateMilestone, resolveInsertMilestone
@strawberryA.federation.type(keys=["id"],description="""Entity representing a milestone""")
class MilestoneGQLModel:
    @classmethod
    async def resolve_reference(cls, info: strawberryA.types.Info, id: strawberryA.ID):
        result = await resolveMilestoneById(AsyncSessionFromInfo(info), id)
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
        result = await resolveProjectById(AsyncSessionFromInfo(info), self.project_id)
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
        result = await resolveProjectsForGroup(AsyncSessionFromInfo(info), self.id)
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
        result = await resolveProjectAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Returns project by its id""")
    async def project_by_id(self, info: strawberryA.types.Info, id: uuid.UUID) -> Union[ProjectGQLModel, None]:
        result = await resolveProjectById(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Returns a list of project types""")
    async def project_type_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[ProjectTypeGQLModel]:
        result = await resolveProjectTypeAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Returns a list of finances""")
    async def finance_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[FinanceGQLModel]:
        result = await resolveFinanceAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Returns a list of finance types""")
    async def finance_type_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[FinanceTypeGQLModel]:
        result = await resolveFinanceTypeAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Returns a list of milestones""")
    async def milestone_page(self, info: strawberryA.types.Info, skip: int = 0, limit: int = 10) -> List[MilestoneGQLModel]:
        result = await resolveMilestoneAll(AsyncSessionFromInfo(info), skip, limit)
        return result

    @strawberryA.field(description="""Returns a list of projects for group""")
    async def project_by_group(self, info: strawberryA.types.Info, id: strawberryA.ID) -> List[ProjectGQLModel]:
        result = await resolveProjectsForGroup(AsyncSessionFromInfo(info), id)
        return result

    @strawberryA.field(description="""Random projects""")
    async def randomProject(self, info: strawberryA.types.Info) -> Union[ProjectGQLModel, None]:
        result = await randomDataStructure(AsyncSessionFromInfo(info))
        return result