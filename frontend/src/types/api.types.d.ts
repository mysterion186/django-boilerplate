
// Interface for authenticate the user that comes from a 3rd part authentication
interface ProviderCredentials extends RawProviderCredential{
    provider: string 
}

// Interface for "basic" user
interface BasicCredentials {
    username: string;
    password: string;
}

// get the raw response of the Provider
export interface RawProviderCredential {
    accessToken: string;
}

export type type_headers = {
    'Content-type' : string;
    authorization? : string;
}

export type Credentials = ProviderCredentials | BasicCredentials;