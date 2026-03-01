const TOKEN_KEY = "access-token"

export function getToken(){
    return localStorage.getItem(TOKEN_KEY) || ''
}

export function deleteToken(){
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem('user-data')
}

export function saveUserData(user: Record<string, any>, access_token: string){
    localStorage.setItem(TOKEN_KEY, access_token);
    localStorage.setItem('user-data', JSON.stringify(user))
}