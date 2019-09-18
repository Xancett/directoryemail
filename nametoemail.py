from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

# Function to get the URL content
def simple_get(url):
	try: # Try to open the url for the content
		with closing(get(url, stream=True)) as resp:
			return resp.content
	except RequestException as e: # Return None if there was an error
		log_error('Error during request')
		return None


# Function to grab the email from a specific name
def GetEmail(fName, lName):
	my_url = 'https://web.cscc.edu/Directory/SearchResults.aspx?LastName=' + lName
	my_email = 'DidNotFind'
	pageRequest = simple_get(my_url)
	page = BeautifulSoup(pageRequest, 'html.parser')
	for i, li in enumerate(page.select('tr')):
		if (li.text.find(fName) != -1):
			my_url = 'https://web.cscc.edu/Directory/' + li.a.get('href')
	pageRequest = simple_get(my_url)
	page = BeautifulSoup(pageRequest, 'html.parser')
	for i, td in enumerate(page.select('td')):
		# Find the email
		if (td.text.find('cscc.edu') != -1):
			my_email = td.get_text()
	return my_email

# Function to loop through a text file, parse data and write out email information
def ReadFile(fileName):
	input = open(fileName, "r") # Open file for read and write
	output = open("output.txt", "w") # Open file for output
	for line in input:
		if (len(line) > 1):
			#Output the First name, last name, and email in a way that can be copy/pasted into excel
			output.write(line.split()[0] + ' ' + line.split()[1] + '\t' + GetEmail(line.split()[0], line.split()[1]) + '\n')
	input.close()
	output.close()


# Main
ReadFile('input.txt') # Reads from the input file and outputs to the output file
