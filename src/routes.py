from .customers import CustomersApi, CustomerApi, CustomerCodeApi
from .users import UserApi, UsersApi
from .login import LoginApi, ForgotPasswordApi, ResetPasswordApi, ChangePasswordApi
from .clients import ClientApi, ClientsApi
from .cases import CaseApi, CasesApi
from .docs import DocApi, DocsApi, AccessDocs
from .notes import NoteApi, NotesApi

def initialize_routes(api):

    # customer model
    api.add_resource(CustomersApi, '/api/v1/customer')
    api.add_resource(CustomerApi, '/api/v1/customer/<id>')
    api.add_resource(CustomerCodeApi, '/api/v1/customer_code/<id>')

    #user model
    api.add_resource(UsersApi, '/api/v1/user')
    api.add_resource(UserApi, '/api/v1/user/<id>')

    #login model
    api.add_resource(LoginApi, '/api/v1/login')
    api.add_resource(ForgotPasswordApi, '/api/v1/forgot_password/<email>')
    api.add_resource(ResetPasswordApi, '/api/v1/reset_password')
    api.add_resource(ChangePasswordApi, '/api/v1/change_password/<id>')


    #client model
    api.add_resource(ClientApi, '/api/v1/client')
    api.add_resource(ClientsApi, '/api/v1/client/<id>')

    #case model
    api.add_resource(CaseApi, '/api/v1/case')
    api.add_resource(CasesApi, '/api/v1/case/<id>')

    #doc modle
    api.add_resource(DocApi, '/api/v1/document')
    api.add_resource(DocsApi, '/api/v1/document/<id>')
    api.add_resource(AccessDocs, '/api/v1/access_document/<id>')

    #notes modle
    api.add_resource(NoteApi, '/api/v1/note')
    api.add_resource(NotesApi, '/api/v1/note/<id>')