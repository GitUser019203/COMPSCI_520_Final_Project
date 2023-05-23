from multiprocessing import cpu_count
from mongoengine import connect
from pycoshark.mongomodels import Project, VCSSystem, Commit
from pycoshark.utils import create_mongodb_uri_string
from Python.NLTK.issueTitlesModel import IssueTitlesModel

# You may have to update this dict to match your DB credentials
credentials = {'db_user': '',
               'db_password': '',
               'db_hostname': 'localhost',
               'db_port': 27017,
               'db_authentication_database': '',
               'db_ssl_enabled': False}

# Create a connection string for MongoDB
uri = create_mongodb_uri_string(**credentials)

# Create a mongoDB client
mongoClient = connect('smartshark_small_2_0', host=uri, alias='default')

# Get the 68 projects from the Mongo DB database
projectCollection = Project.objects()

# Initialize an issue titles model
issue_titles_model = IssueTitlesModel()

for j, project in enumerate(projectCollection):
    print(f'Starting mining #{j}: {project.name}')
    # We now select the version control system of the project
    vcs_system = VCSSystem.objects(project_id=project.id).get()

    # We can now grab the commits in the VCS system
    commits = Commit.objects(vcs_system_id=vcs_system.id)

    for commit in commits:
        #commit_queue.put(commit)

        # Mine the commit and store extracted information in the model
        issue_titles_model.mine_commit(commit)

    #for i in range(0, 2):
    #    Thread(target = issue_titles_model.commit_mining_worker, daemon = True).start()
    #commit_queue.join()
    print(f'Completed mining #{j}: {project.name}')

# Save the model to disk
issue_titles_model.save()
