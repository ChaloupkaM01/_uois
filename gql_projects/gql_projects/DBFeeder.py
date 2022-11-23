from doctest import master
from functools import cache
from gql_projects.DBDefinitions import BaseModel, ProjectModel, ProjectTypeModel, FinanceModel, FinanceTypeModel, MilestoneModel, GroupModel

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
        {'name':'shortTerm'},
        {'name':'mediumTerm'},
        {'name':'longTerm'},
    ]
    return projectTypes

def determineFinanceTypes():
    """Definuje zakladni typy financi"""
    financeTypes = [ 
        {'name':'travel_expenses'},
        {'name':'accomodation_expenses'},
        {'name':'other_expenses'},
    ]
    return financeTypes

def randomProject(name):
    result = {
        'name': {name},
        #'startDate': randomDate()
        #'endDate': randomDate()
        'milestones' : [
            #randomMilestone(i+1) for i in range(random.randint(3, 5))
        ],
    }
    return result

    def randomMilestone(index):
        result = {
            'name': f'Milestone {index}'
            #'startDate': randomDate(),
            #'endDAte' :  randomDate(),

        }
        return result
    
    def randomFinance():
        result = {
            'name':'',
            'amount': random.randint(100, 20000),
        }
        return result