import boto3
import os

def lambda_handler(event, context):
    cc = boto3.client('codecommit')
    file = 'This is the README for the Project'

    cc.create_commit(
    repositoryName= os.environ['REPOSITORY'],
    branchName= os.environ['MAIN'],
    authorName= os.environ['AUTHOR'],
    email= os.environ['EMAIL'],
    commitMessage= os.environ['COMMITMESSAGE'],
    putFiles=[
        {
            'filePath': 'README.md',
            'fileMode': 'NORMAL',
            'fileContent': file
        }
    ])

    response = cc.get_branch(
    repositoryName= os.environ['REPOSITORY'],
    branchName= os.environ['MAIN']
    )
    CommitId = (response['branch']['commitId'])

    cc.update_default_branch(
    repositoryName= os.environ['REPOSITORY'],
    defaultBranchName= os.environ['MAIN']
    )

    cc.create_branch(
    repositoryName= os.environ['REPOSITORY'],
    branchName= os.environ['STAGING'],
    commitId= CommitId
    )

