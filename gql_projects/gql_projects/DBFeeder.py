from gql_projects.DBDefinitions import BaseModel, ProjectModel, ProjectTypeModel, FinanceModel, FinanceTypeModel, MilestoneModel, GroupModel

import uuid
import random
import itertools

from functools import cache
from datetime import date, timedelta


from sqlalchemy.future import select

def singleCall(asyncFunc):
    """Dekorator, ktery dovoli, aby dekorovana funkce byla volana (vycislena) jen jednou. Navratova hodnota je zapamatovana a pri dalsich volanich vracena.
       Dekorovana funkce je asynchronni.
    """
    resultCache = {}
    async def result():
        if resultCache.get('result', None) is None:
            resultCache['result'] = await asyncFunc()
        return resultCache['result']
    return result

###########################################################################################################################
#
# zde definujte sve funkce, ktere naplni random data do vasich tabulek
#
###########################################################################################################################

def randomUUID(limit):
    userIDs = [uuid.uuid4() for _ in range(limit)]
    return userIDs

def randomStartDate():
    base = date(2020, 1, 1)
    return base + timedelta(days=random.randint(1,50))

def randomEndDate(startDate):
    return startDate + timedelta(days=random.randint(50,100))

def randomProjectName():
    names = ["Informacni system", "Lesaci", "Wow grind", "SPZ", "Vault of Incarnates"]
    return random.choice(names)

projectTypesIDs = randomUUID(3)
financeTypesIDs = randomUUID(3)
projectIDs = randomUUID(2)
financeIDs = randomUUID(10)
milestoneIDs = randomUUID(10)

def determineProjectTypes(ids):
    """Definuje zakladni typy roli"""  
    projectTypes = [ 
        {'id': projectTypesIDs[0], 'type':'shortTerm'},
        {'id': projectTypesIDs[1], 'type':'mediumTerm'},
        {'id': projectTypesIDs[2], 'type':'longTerm'},
    ]
    return projectTypes

def determineFinanceTypes(ids):
    """Definuje zakladni typy financi"""
    financeTypes = [ 
        {'id': financeTypesIDs[0], 'type':'travelExpenses'},
        {'id': financeTypesIDs[1], 'type':'accomodationExpenses'},
        {'id': financeTypesIDs[2], 'type':'otherExpenses'},
    ]
    return financeTypes

def randomProject(id):
    """Náhodný projekt"""
    startDate = randomStartDate()
    return {
        'id': id,
        'name': randomProjectName(),
        'startDate': startDate,
        'endDate': randomEndDate(startDate),
        'lastChange': date.today(),

        'projectType_id': random.choice(projectTypesIDs),

        'group_id': '' #externalID
    }

def randomFinance(id, index):
    """Náhodné finance"""
    return {
        'id': id,
        'name': f'Finance {index}',
        'amount': random.randint(100, 20000),
        'lastChange': date.today(),

        'project_id': random.choice(projectIDs),

        'financeType_id': random.choice(financeTypesIDs)    
    }

def randomMilestone(id, index):
    """Náhodný milestone"""
    return {
        'id': id,
        'name': f'Milestone {index}',
        'date': randomStartDate(),
        'lastChange': date.today(),

        'project_id': random.choice(projectIDs)
    }

def createDataStructureProjectTypes():
    projectTypes = determineProjectTypes()
    return projectTypes

def createDataStructureFinanceTypes():
    financeTypes = determineFinanceTypes()
    return financeTypes

def createDataStructureProjects():
    projects = [randomProject(id) for id in projectIDs]
    return projects

def createDataStructureFinances():
    index = 1
    finances = []
    for id in financeIDs:
        finances.append(randomFinance(id,index))
        index = index + 1

    return finances  

def createDataStructureMilestones():
    index = 1
    milestones = []
    for id in milestoneIDs:
        milestones.append(randomMilestone(id,index))
        index = index + 1

    return milestones

async def randomDataStructure(session):

    projectTypes = createDataStructureProjectTypes()
    projectTypesToAdd = [ProjectTypeModel(**record) for record in projectTypes]
    async with session.begin():
        session.add_all(projectTypesToAdd)
    await session.commit()
    
    financeTypes = createDataStructureFinanceTypes()
    financeTypesToAdd = [FinanceTypeModel(**record) for record in financeTypes]
    async with session.begin():
        session.add_all(financeTypesToAdd)
    await session.commit()
    
    projects =  createDataStructureProjects()
    projectsToAdd = [ProjectModel(**record) for record in projects]
    async with session.begin():
        session.add_all(projectsToAdd)
    await session.commit()

    finances =  createDataStructureFinances()
    financesToAdd = [FinanceModel(**record) for record in finances]
    async with session.begin():
        session.add_all(financesToAdd)
    await session.commit()

    milestones =  createDataStructureMilestones()
    milestonesToAdd = [MilestoneModel(**record) for record in milestones]
    async with session.begin():
        session.add_all(milestonesToAdd)
    await session.commit()
