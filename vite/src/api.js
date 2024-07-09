import MD5 from "crypto-js/md5.js";

export function fetchJSON(url, token) {
    return fetch(url, {
        method: 'GET',
        headers: {'X-CSRF-Token': token}
    }).then(r => r.json());
}

export function fetchResponse(url, token) {
    return fetch(url, {
        method: 'GET',
        headers: {'X-CSRF-Token': token}
    });
}

/**
 * @param ref Reference to json
 * @returns {Promise<void>}
 */
export async function fetchProfile(ref) {
    let response = await fetch("/api/auth/profile/");

    if (!response.ok) {
        ref.value = null;
        return;
    }

    ref.value = await response.json();
}

export function getGravatarHash(email) {
    return MD5(email.trim().toLowerCase());
}
