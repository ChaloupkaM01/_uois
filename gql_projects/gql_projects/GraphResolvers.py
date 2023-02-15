
from ast import Call
from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy import delete
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import create1NGetter, createEntityByIdGetter, createEntityGetter, createInsertResolver, createUpdateResolver
from uoishelpers.resolvers import putSingleEntityToDb

## Nasleduji funkce, ktere lze pouzit jako asynchronni resolvery

###########################################################################################################################
#
# zde si naimportujte sve SQLAlchemy modely
#
###########################################################################################################################

from gql_projects.DBDefinitions import BaseModel
from gql_projects.DBDefinitions import ProjectModel, ProjectTypeModel, FinanceModel, FinanceTypeModel, MilestoneModel, GroupModel

###########################################################################################################################
#
# zde definujte sve resolvery s pomoci funkci vyse
# tyto pouzijete v GraphTypeDefinitions
#
###########################################################################################################################

#Project resolvers
resolveProjectById = createEntityByIdGetter(ProjectModel)
resolveProjectAll = createEntityGetter(ProjectModel)
resolveUpdateProject = createUpdateResolver(ProjectModel)
resolveInsertProject = createInsertResolver(ProjectModel)

resolveMilestonesForProject = create1NGetter(MilestoneModel, foreignKeyName='project_id')
resolveFinancesForProject = create1NGetter(FinanceModel, foreignKeyName='project_id')

#ProjectType resolvers
resolveProjectTypeById = createEntityByIdGetter(ProjectTypeModel)
resolveProjectTypeAll = createEntityGetter(ProjectTypeModel)
resolveUpdateProjectType = createUpdateResolver(ProjectTypeModel)
resolveInsertProjectType = createInsertResolver(ProjectTypeModel)

resolveProjectsForProjectType = create1NGetter(ProjectModel, foreignKeyName='projectType_id')

#Finance resolvers
resolveFinanceById = createEntityByIdGetter(FinanceModel)
resolveFinanceAll = createEntityGetter(FinanceModel)
resolveUpdateFinance = createUpdateResolver(FinanceModel)
resolveInsertFinance = createInsertResolver(FinanceModel)

async def resolveRemoveFinance(session, project_id, finance_id):
    stmt = delete(FinanceModel).where((FinanceModel.project_id==project_id) & (FinanceModel.id==finance_id))
    resultMsg= ""
    try:
        response = await session.execute(stmt)
        await session.commit()
        if(response.rowcount == 1):
            resultMsg = "ok"
        else:
            resultMsg = "fail"
        
    except:
        resultMsg="error"
  
    return resultMsg


#FinanceType resolvers
resolveFinanceTypeById = createEntityByIdGetter(FinanceTypeModel)
resolveFinanceTypeAll = createEntityGetter(FinanceTypeModel)
resolveUpdateFinanceType = createUpdateResolver(FinanceTypeModel)
resolveInsertFinanceType = createInsertResolver(FinanceTypeModel)

resolveFinancesForFinanceType = create1NGetter(FinanceModel, foreignKeyName='financeType_id')

#Milestone resolvers
resolveMilestoneById = createEntityByIdGetter(MilestoneModel)
resolveMilestoneAll = createEntityGetter(MilestoneModel)
resolveUpdateMilestone = createUpdateResolver(MilestoneModel)
resolveInsertMilestone = createInsertResolver(MilestoneModel)

async def resolveRemoveMilestone(session, project_id, milestone_id):
    stmt = delete(MilestoneModel).where((MilestoneModel.project_id==project_id) & (MilestoneModel.id==milestone_id))
    resultMsg= ""
    try:
        response = await session.execute(stmt)
        await session.commit()
        if(response.rowcount == 1):
            resultMsg = "ok"
        else:
            resultMsg = "fail"
        
    except:
        resultMsg="error"
  
    return resultMsg


#Group resolvers
resolveProjectsForGroup = create1NGetter(ProjectModel, foreignKeyName='group_id')