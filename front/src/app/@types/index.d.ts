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

export type tProduct = {
    id: number,
    name: string,
    mark: string,
    value: number
    created_at: string,
    updated_at: string,
}

export type tDataProduct = {
    data: tProduct[],
    success: true,
}

export type tProductRes = {
    data: {
        message: string,
        success: true,
    } 
    status: number
}

export type tCreateProductMsg = tProductRes;

export type tDeleteProductMsg = tProductRes;

export type tEditProductMsg = tProductRes;