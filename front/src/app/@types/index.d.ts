export type tErroRequest = {
    error: {
        message: string,
        status_code: number,
        type: string
    },
    success: false
}

export type tDataLogin = {
    access_token: string,
    user: {
        email: string,
        id: number,
        name: string,
        created_at: string,
        updated_at: string,
    }
}
