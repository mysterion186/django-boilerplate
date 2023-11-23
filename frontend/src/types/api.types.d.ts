
// Interface for authenticate the user that comes from a 3rd part authentication
interface ProviderCredentials extends RawProviderCredential{
    provider: string 
}

// Interface for "basic" user
interface BasicCredentials {
    email: string;
    password: string;
}

// type for handling user's registration
export type UserRegistration= {
    email: string,
    password: string, 
    password1: string,
    biography: string
}

// get the raw response of the Provider
export interface RawProviderCredential {
    access_token: string;
}

export interface RawProviderCredentialCamelCase {
    accessToken: string;
}
export type UserPasswordUpdate = {
    old_password: string,
    password: string, 
    password1: string
}

export interface OptionalUserInformation {
    biography: string
}

export interface UserInformation {
    email: string,
    biography: string | null
}
export type type_headers = {
    'Content-type' : string;
    authorization? : string;
}

export type Credentials = ProviderCredentials | BasicCredentials;