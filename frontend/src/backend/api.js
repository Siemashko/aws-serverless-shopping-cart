import {API, Auth} from 'aws-amplify'

async function getHeaders(includeAuth) {
    const headers = {
        "Content-Type": "application/json"
    }

    if (!includeAuth) {
        return {
            "Content-Type": "application/json"
        }
    }
    let session = null
    try {
        session = await Auth.currentSession()
    } catch (e) {
        e == e
    }
    if (session) {
        let authheader = session.getIdToken().jwtToken
        headers['Authorization'] = authheader
    }
    return headers
}

export async function getCart() {
    return getHeaders(true).then(
        headers => API.get("CartAPI", "/cart", {
            headers: headers,
            withCredentials: true
        }))
}

export async function postCart(obj, quantity = 1) {
    return getHeaders(true).then(
        headers => API.post("CartAPI", "/cart", {
            body: {
                productId: obj.productId,
                quantity: quantity,
            },
            headers: headers,
            withCredentials: true
        })
    )
}

export async function putCart(obj, quantity) {
    return getHeaders(true).then(
        headers => API.put("CartAPI", "/cart/" + obj.productId, {
            body: {
                productId: obj.productId,
                quantity: quantity,
            },
            headers: headers,
            withCredentials: true
        })
    )
}

export async function getProducts(filterParams) {

    let queryParams = {};
    if (filterParams) {
        if (filterParams.c.length > 0) {
            queryParams.c = filterParams.c.join(",");
        }
        if (filterParams.p) {
            queryParams.pl = filterParams.p[0]*100;
            queryParams.ph = filterParams.p[1]*100;
        }
    }

    return getHeaders().then(
        headers => API.get("ProductAPI", "/product", {
            headers: headers,
            queryStringParameters: queryParams
        })
    )
}

export async function getProduct(productId) {
    return getHeaders().then(
        headers => API.get("ProductAPI", "/product/" + productId, {
            headers: headers
        })
    )
}

export async function cartMigrate() {
    return getHeaders(true).then(
        headers => API.post("CartAPI", "/cart/migrate", {
            headers: headers,
            withCredentials: true
        })
    )
}

export async function cartCheckout() {
    return getHeaders(true).then(
        headers => API.post("CartAPI", "/cart/checkout", {
            headers: headers,
            withCredentials: true
        })
    )
}

export async function cartDelete() {
    return getHeaders(true).then(
        headers => API.post("CartAPI", "/cart/delete", {
            headers: headers,
            withCredentials: true
        })
    )
}