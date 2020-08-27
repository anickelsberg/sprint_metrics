# This script shows how to connect to a JIRA instance with a
from jira import JIRA
import pprint
import urllib3
import re
import csv
urllib3.disable_warnings() #yolo

username = "XX"
password = "XX"
 
# Connect to the Wayfair instance (ProjectHub)
jira = JIRA(options={'server':'XX', 'verify':XX}, basic_auth=(username, password))


issues_in_project = jira.search_issues('project = "XX" AND (sprint in openSprints() OR sprint in closedSprints())', maxResults = -1)

count = 0

with open('jira_data_2.csv','w') as data_file:
	csv_writer = csv.writer(data_file)
	for issue in issues_in_project:
		sprint_id = issue.fields.customfield_10100
		issue_id = issue.key
		done_date = issue.fields.resolutiondate
		issue_name = issue.fields.summary
		label = issue.fields.labels
		active_sprint = re.findall(r"name=[^,]*", [str(sprint) for sprint in sprint_id][-1])[0].split("=")[1]
		try:
			story_points = issue.fields.customfield_10106
		except AttributeError:
			story_points = 0
		for sprints in sprint_id:
			sprint_names = re.findall(r"name=[^,]*",str(sprints))
			for sprint_name in sprint_names:
				type = sprint_name.split("=")
				sprint_number = type[1]			 	
				if sprint_number == active_sprint:
					done_points = story_points
				else:
					done_points = 0
				if count == 0:
					header = "IssueName","IssueId","SprintName","LastSprint","StoryPoints","DonePoints","Label"
					csv_writer.writerow(header)
					count += 1
				csv_writer.writerow([issue_name,issue_id,sprint_number,active_sprint,story_points,done_points,label])
				print(csv_writer)