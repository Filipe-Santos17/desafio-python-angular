import { tErroRequest } from "../@types";

type tHttpMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';

type tRoute = {
    method: tHttpMethod,
    hasBody: boolean,
    route: string,
}

type tAllowedRoutes = Record<string, tRoute>

type tOptionsRequest = {
    includesToken?: boolean,
    specificId?: number | string,
    headers?: RequestInit['headers'], 
}

const allowedRoutes = {
    "auth-login": {
        method: "POST",
        hasBody: true,
        route: "auth/login",
    },
    "auth-register":{
        method: "POST",
        hasBody: true,
        route: "auth/register",
    },
    "product-register":{
        method: "POST",
        hasBody: true,
        route: "products",
    },
    "product-get":{
        method: "GET",
        hasBody: false,
        route: "products",
    },
    "product-remove":{
        method: "DELETE",
        hasBody: false,
        route: "products",
    },
    "product-change":{
        method: "PUT",
        hasBody: true,
        route: "products",
    },
} as const satisfies tAllowedRoutes;

export async function globalFetch<T, R>(
    router: keyof typeof allowedRoutes, 
    data: T | null = null, 
    options?: tOptionsRequest
){
    const requestInfo = allowedRoutes[router] || null

    if(!requestInfo) throw new Error("Router not allowed")

    const routeOptions = options || {
        headers: null,
        includesToken: true,
        specificId: null
    }

    const { hasBody, method, route } = requestInfo

    const requestContent: RequestInit = {
        method,
        credentials: 'include',
    }

    if(hasBody && !(["GET", "DELETE"].includes(method))){
        requestContent.body = JSON.stringify(data)
        requestContent.headers = {
            'Content-Type': 'application/json',
        }
    }

    if(routeOptions?.headers){
        const token = localStorage.getItem("acess-token")

        requestContent.headers = {
            ...requestContent.headers, 
            ...routeOptions.headers,
            Authorization: routeOptions?.includesToken ? `Bearer ${token}` : ''
        }
    }

    const baseRoute = 'https://localhost/api/'

    const id = routeOptions?.specificId

    const requestRouter = `${baseRoute}${route}${id ? `/${id}` : ''}`

    const response = await fetch(requestRouter, requestContent);

    if (!response.ok) {
        const errorData = await response.json() as tErroRequest;

        const formattedMessage = `${errorData.error.message} - ${errorData.error.type}`;

        const customError = new Error(formattedMessage);

        (customError as any).status = errorData.error.status_code;
        (customError as any).type = errorData.error.type;

        throw customError;
    }

    const responseStatus = response.status
    const responseData = await response.json() as R;

    return {data: responseData, status: responseStatus}
}

