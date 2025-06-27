import asyncio
from azure.identity.aio import ClientSecretCredential
from msgraph.generated.users.users_request_builder import UsersRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from datetime import datetime,timedelta,timezone
from msgraph import GraphServiceClient

#If you want to use Automation (For example sending mail), don't use ClientSecretCredential - instead use DefaultAzureCredential for your system managed identity
credential = ClientSecretCredential(
    tenant_id='YOUR TENANT ID',
    client_id='YOUR CLIENT ID',
    client_secret='YOUR CLIENT SECRET'
)
scopes = ['https://graph.microsoft.com/.default']
client = GraphServiceClient(credentials=credential, scopes=scopes)
query_params = UsersRequestBuilder.UsersRequestBuilderGetQueryParameters(
    select=["displayName","userPrincipalName","signInActivity","id","accountEnabled","onPremisesSyncEnabled","createdDateTime"]
)

request_configuration = RequestConfiguration(
    query_parameters=query_params
)

async def get_admins():
    roles = await client.directory_roles.get()
    for role in roles.value:
        print(f"\n🔒 Role: {role.display_name}")
        
        members = await client.directory_roles.by_directory_role_id(role.id).members.get()
        for member in members.value:
            user = await client.users.by_user_id(member.id).get(request_configuration=request_configuration)
            if user.sign_in_activity and user.sign_in_activity.last_sign_in_date_time:
                last_sign_in = user.sign_in_activity.last_sign_in_date_time
                formatted_date = last_sign_in.strftime("%Y-%m-%d")
                created_date = user.created_date_time
                fromatted_created_date = created_date.strftime("%Y-%m-%d")
                print(f"UPN: {user.user_principal_name} - accountEnabled: {user.account_enabled} - on-premise sync: {user.on_premises_sync_enabled} - Created: {fromatted_created_date} - Last Sign-in: {formatted_date}")
            else:
                print(f"UPN: {user.user_principal_name} - accountEnabled: {user.account_enabled} - on-premise sync: {user.on_premises_sync_enabled} - Created: {fromatted_created_date} - Last Sign-in: None")

asyncio.run(get_admins())
