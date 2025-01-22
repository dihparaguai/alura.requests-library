from math import ceil
import pandas as pd
import requests
import base64
from my_config import PRIVATE_TOKEN


class DadosRepo():
    def __init__(self, owner):
        self.owner_user = owner
        self.headers = {
            'X-GitHub-Api-Version': '2022-11-28',
            'Authorization': f'Bearer {PRIVATE_TOKEN}'
        }
        self.url_base = 'https://api.github.com/'
        self.owner_name = self.get_owner_name()
        self.total_pages = self.get_total_pages()
        self.repos_list = self.get_repos_list()
        self.file_path = f'{self.owner_name}_dataset_repos_name_and_language_with_python_class.csv'

    # get the profile user's information 
    def get_users_profile(self):
        url = f'{self.url_base}/users/{self.owner_user}'
        response = requests.get(url, headers=self.headers)
        return response.json()

    # get the user's name
    def get_owner_name(self):
        owmer_name = self.get_users_profile()['name']
        return owmer_name.lower()

    # get the total number of repositories and divide by 30 to get the total number of pages
    def get_total_pages(self):
        total_repos = self.get_users_profile()['public_repos']
        return ceil(total_repos/30)

    # get all the repositories
    def get_repos_list(self):
        repos_list = []
        page = 1
        url = f'{self.url_base}/users/{self.owner_user}/repos'

        for page in range(1, self.total_pages+1):
            try:
                url_page = f'{url}?page={page}'
                response = requests.get(url_page, headers=self.headers).json()
                repos_list.append(response)
                page += 1
            except:
                break

        return repos_list

    # get the names from each repository
    def get_repos_name(self):
        repos_names = []

        while True:
            for page in self.repos_list:
                for repo in page:
                    repos_names.append(repo['name'])
            break

        return repos_names

    # get the language's name from each repository 
    def get_repos_language(self):
        repos_languages = []

        for page in self.repos_list:
            for repo in page:
                repos_languages.append(repo['language'])

        return repos_languages

    # create a CSV file with the repositories' names and languages
    def create_dataset(self):
        data = {
            'repo_names': self.get_repos_name(),
            'repos_language': self.get_repos_language()
        }
        
        df = pd.DataFrame(data)
        print(df)
        df.to_csv(self.file_path, index=False)

    # send the CSV file to the github repository 
    def send_to_github(self, owner_user, repo_name, commit_message):
        url = f'{self.url_base}/repos/{owner_user}/{repo_name}/contents/{self.file_path}'

        with open(self.file_path, 'rb') as file:
            enconded_content = base64.b64encode(file.read())

        data = {
            'message': commit_message,
            'content': enconded_content.decode('utf-8')
        }

        try:
            response = requests.put(url, headers=self.headers, json=data)
            if int(response.status_code) in range(200, 300):
                print(f'tudo certo! ({response.status_code})')
            else:
                print(f'erro!!! ({response.status_code})')
        except:
            print(f'erro!!! ({response.status_code})')


# instantiete the object, create the CSV file dataset and send to the github repository 
repo_amazon = DadosRepo('amzn')
repo_amazon.create_dataset()
repo_amazon.send_to_github(
    'dihparaguai',
    'alura.python-e-apis-conhecendo-a-biblioteca-requests-files',
    'adicionar dataset feito com classe em Python'
)

repo_netflix = DadosRepo('netflix')
repo_netflix.create_dataset()
repo_netflix.send_to_github(
    'dihparaguai',
    'alura.python-e-apis-conhecendo-a-biblioteca-requests-files',
    'adicionar dataset feito com classe em Python'
)

repo_spotify = DadosRepo('spotify')
repo_spotify.create_dataset()
repo_spotify.send_to_github(
    owner_user='dihparaguai',
    repo_name='alura.python-e-apis-conhecendo-a-biblioteca-requests-files',
    commit_message='adicionar dataset feito com classe em Python'
)

repo_uber = DadosRepo('uber-go')
repo_uber.create_dataset()
repo_uber.send_to_github(
    owner_user='dihparaguai',
    repo_name='alura.python-e-apis-conhecendo-a-biblioteca-requests-files',
    commit_message='adicionar dataset feito com classe em Python'
)
