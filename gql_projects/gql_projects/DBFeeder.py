from gql_projects.DBDefinitions import BaseModel, ProjectModel, ProjectTypeModel, FinanceModel, FinanceTypeModel, MilestoneModel, GroupModel

import uuid
import random
import itertools

from functools import cache


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

def determineProjectTypes():
    """Definuje zakladni typy roli"""
    projectTypes = [ 
        {'id': f'{uuid.uuid1()}', 'name':'shortTerm'},
        {'id': f'{uuid.uuid1()}', 'name':'mediumTerm'},
        {'id': f'{uuid.uuid1()}', 'name':'longTerm'},
    ]
    return projectTypes

def determineFinanceTypes():
    """Definuje zakladni typy financi"""
    financeTypes = [ 
        {'id': f'{uuid.uuid1()}', 'name':'travel_expenses'},
        {'id': f'{uuid.uuid1()}', 'name':'accomodation_expenses'},
        {'id': f'{uuid.uuid1()}', 'name':'other_expenses'},
    ]
    return financeTypes

def randomProject(name):
    """Náhodný projekt"""
    randomGroupResult = randomGroup()

    result = {
        'id': f'{uuid.uuid1()}',
        'name': f'{name}',
        #'startDate': randomDate()
        #'endDate': randomDate()
        'projectType_id': "",
        'finances' : [
            #randomFinance(i+1) for i in range(random.randint(3, 5))
        ],

        'milestones' : [
            #randomMilestone(i+1) for i in range(random.randint(3, 5))
        ],
        'group_id': randomGroupResult['id']
    }
    return result

def randomFinance(index):
    """Náhodné finance"""
    randomProjectResult = randomProject()

    result = {
        'id': f'{uuid.uuid1()}',
        'name': f'Finance{index}',
        'amount': random.randint(100, 20000),
        'financeType_id': '',

        'project_id': randomProjectResult['id'],
    }
    return result

def randomMilestone(index):
    """Náhodný milestone"""
    randomProjectResult = randomProject()

    result = {
        'id': f'{uuid.uuid1()}',
        'name': f'Milestone {index}',
        #'startDate': randomDate(),
        #'endDAte' :  randomDate(),

        'project_id': randomProjectResult['id'],
    }
    return result

def randomGroup():
    """Náhodná řešitelská skupina"""
    result = {
        'id': f'{uuid.uuid1()}',
    }
    return result