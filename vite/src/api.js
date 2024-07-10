import MD5 from "crypto-js/md5.js";
import {ref} from "vue";

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

export class Form {
    "use strict"

    processing = false;
    errors = {};
    _inputs = [];

    constructor(data) {
        let _data = data;

        if (Array.isArray(data)) {
            _data = {};

            for (const element of data) {
                _data[element] = '';
            }
        }

        for (const input in _data) {
            this._inputs.push(input);
            this.errors[input] = ref('');
            this[input] = _data[input];
        }

        this.processing = false;
    }

    data() {
        let data = {};

        for (let input of this._inputs) {
            data[input] = this[input];
        }
        return data;
    }

    setError(input, error) {
        let ref = this.errors[input];

        if (ref) {
            ref.value = error;
        } else {
            alert(error);
        }
    };

    submit(method, url) {
        let options = {
            method: method,
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(this.data()),
        };

        fetch(url, options).then(r => this._process(r))
        console.log(this.data());
    };

    post(url) {
        this.submit('POST', url);
    }

    put(url) {
        this.submit('PUT', url);
    }

    patch(url) {
        this.submit('PATCH', url);
    }

    delete(url) {
        this.submit('DELETE', url);
    }

    _process(response) {
        console.assert(response);

        if (!response.ok) {
            console.error(response);
            response.json().then(json => this._processError(json));
        }
    }

    _processError(json) {
        for (const input in json) {
            this.setError(input, json[input][0]);
        }
    }
}

export function useForm(data) {
    return new Form(data);
}
