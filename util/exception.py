class ExceptionMessages:
    NotAdminException = "User is not an admin"
    CustomerInactive = "Customer is inactive"
    InvalidCustomerCode = "Invalid Customer Code"
    CustomerNotExist = "Customer not exist"
    UserNotExist = "User not exist"
    UserInactive = "User is inactive"
    InvalidPassword = "Invalid Password"
    AuthTokenExpired = "Auth token expired"
    InvaliAuthToken = "Invalid Auth token"
    UnauthorizedUser = "Unauthorized User"
    ClientInactive = "Client is Inactive"
    ClientNotExist = "Clinet not exist"
    FileUploadFail = "File uploading is fail"
    InvalidRequestSchema = "Invalid request data"
    CaseNotExist = "Case not exist"
    DocumentNotExist = "Document not exist"
    NotesNotExist = "Notes not exist"
    FileTypeNotAllowed = "File type not allowed"
    

class InvaliAuthToken(Exception):
    pass
