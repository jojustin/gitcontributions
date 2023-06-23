import requests
import os
from datetime import datetime, timedelta
from tabulate import tabulate

git_header = {"Authorization": f"Bearer {os.environ.get('GH_TOKEN')}"}
git_url = "https://api.github.com/graphql"

def run_query(url, header, query, variables):
    request = requests.post(url, json={'query': query, 'variables': variables}, headers=header)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))


query = '''
    query($username: String!, $from : DateTime!, $to: DateTime! ) {
        user(login: $username) { 
            contributionsCollection(from: $from, to: $to) {
                contributionCalendar {
                    totalContributions
                }
            }
        }
    }
'''

users = ["jojustin"]  #List of your organization users
user_insights = [] 
range=100 #Date range to retrieve contributions
now_str = (datetime.now()).strftime("%Y-%m-%dT%H:%M:%S")
n_days_ago_str = (datetime.now() - timedelta(days=range)).strftime("%Y-%m-%dT%H:%M:%SZ")
input_variables = {}
input_variables['from'] = n_days_ago_str
input_variables['to'] = now_str

for user in users:
    input_variables['username'] = user
    resp_data = run_query(git_url, git_header, query, input_variables)
    user_contributions  = resp_data['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions']
    user_insights.append([user, user_contributions])        

head = ["User", "Contributions"]
print(tabulate(user_insights, headers=head, tablefmt="grid"))
