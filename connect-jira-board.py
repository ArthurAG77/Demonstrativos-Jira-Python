import pandas as pd
from IPython.display import display
from jira import JIRA
from datetime import datetime

#connect to board
api_key = 'hehe'

jira = JIRA(server='https://nelogicaproject.atlassian.net/', basic_auth=('login_email', api_key))

#sort issues from date to date please follow the model Year/Mounth/Day
start = '2024-05-09'
end = '2024-05-30'


try: #search for issues 
    issues = jira.search_issues(f'project=NELODATA AND created >= "{start}" AND created <= "{end}"')
except:
    print(1) #i will add a interface text to return error if, has no issues from date to date

#list to append all need information
issue_data = []

try:
    for issue in issues:
            #date that issue was created
            create_date = pd.to_datetime(issue.fields.created).date()
            #actual date
            current = datetime.now().date()

            if issue.fields.resolutiondate is not None: #check if issue is ended
                 end_date = pd.to_datetime(issue.fields.resolutiondate).date() #get the issue end date
                 time_to_solve = (end_date - create_date)#calculate how many days take to solve the issue
                 progress = None #return progress as none cause the issue was ended
            else:
                 end_date = issue.fields.resolution #if issue is not solved return 'NaT'
                 time_to_solve = None #return none cause the issue isn't solved 
                 progress = (current - create_date) # count how many days the issue is open

            #create a dictionary with all informations above 
            issue_data.append ({
                'Quantidade_issue': len(issues),
                'Criada' : create_date,
                'Resolvida' : end_date,
                'Atual' : current,
                'Resolução' : time_to_solve,
                'Andamento' : progress
            })
except:
    print(2) 

try:
    df = pd.DataFrame(issue_data)
    display(df)

except:
    print(3)