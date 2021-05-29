import {
    Auth,
    API
} from 'aws-amplify'
import jwt_decode from "jwt-decode";

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

export async function getEmail() {
    let session = null
    try {
        session = await Auth.currentSession()
    } catch (e) {
        e == e
    }
    let customerEmail = null;
    if (session) {
        let token = session.getIdToken().jwtToken;
        let decoded = jwt_decode(token);
        customerEmail = decoded["email"];
    }
    return customerEmail;
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

export async function getProducts() {
    return getHeaders().then(
        headers => API.get("ProductAPI", "/product", {
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