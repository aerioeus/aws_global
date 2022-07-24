import logging
from crhelper import CfnResource
import boto3

logger = logging.getLogger(__name__)

helper = CfnResource(
	json_logging=False,
	log_level='DEBUG',
	boto_level='CRITICAL'
)


def handler(event, context):
    helper(event, context)

try:
    pass
except Exception as e:
    helper.init_failure(e)

@helper.create
def create(event, context):
    logger.info("Resource Created")
    # The CF Resource properties are passed as a json
    # object in the event.
    repositoryName = event['ResourceProperties']['repositoryName']
    mainBranch = event['ResourceProperties']['MainRepo']
    branchName = event['ResourceProperties']['branchName']
    authorName = event['ResourceProperties']['authorName']
    email = event['ResourceProperties']['email']
    commitMessage = event['ResourceProperties']['commitMessage']
    stagingRepo = event['ResourceProperties']['stagingRepo']
    loglevel = event['ResourceProperties']['loglevel']
    logger.info(f'Attempting to create {branchName} inside {repositoryName}')
    file = 'This is the README for the Project'
    cc = boto3.client('codecommit')
    cc.create_commit(
                    putFiles=[
                        {
                            'filePath': 'README.md',
                            'fileMode': 'NORMAL',
                            'fileContent': file
                        }
                    ])

    main_branch = cc.get_branch(
        repositoryName=repositoryName,
        branchName=mainBranch
    )
    CommitId = (main_branch['branch']['commitId'])

    cc.update_default_branch(
        repositoryName=repositoryName,
        defaultBranchName= mainBranch
    )

    cc.create_branch(
        repositoryName=repositoryName,
        branchName=stagingRepo,
        commitId=CommitId
    )
    # Items stored in helper.Data will be saved
    # as attributes you can reference in CloudFormation.
    helper.Data.update({"Commit": f'${commitMessage}'})

    # To return an error to cloudformation you raise an exception:
    if not helper.Data.get("test"):
        raise ValueError("this error will show in the cloudformation events log and console.")

    return True

    @helper.update
    def update(event, context):
        logger.info("Got Update")
        # If the update resulted in a new resource being created, return an id for the new resource. 
        # CloudFormation will send a delete event with the old id when stack update completes
        return True

    @helper.delete
    def delete(event, context):
        logger.info("Got Delete")
        # Delete never returns anything. Should not fail if the underlying resources are already deleted.
        # Desired state.
        return True

    @helper.poll_create
    def poll_create(event, context):
        logger.info("Got create poll")
        # Return a resource id or True to indicate that creation is complete. if True is returned an id 
        # will be generated
        return True
