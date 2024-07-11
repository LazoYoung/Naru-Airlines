import MD5 from "crypto-js/md5.js";
import {ref} from "vue";
import router from "@/router/index.js";

// export function fetchJSON(url, token) {
//     return fetch(url, {
//         method: 'GET',
//         headers: {'X-CSRF-Token': token}
//     }).then(r => r.json());
// }
//
// export function fetchResponse(url, token) {
//     return fetch(url, {
//         method: 'GET',
//         headers: {'X-CSRF-Token': token}
//     });
// }

/**
 * @param ref Reference to json
 * @returns {Promise<void>}
 */
// todo: elevate security measure
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

export function getCookie(name) {
    const regex = new RegExp(`(^| )${name}=([^;]+)`);
    const match = document.cookie.match(regex);

    if (!match) {
        throw new Error(`Cookie '${name}' not found`);
    }
    return match[2];
}

export function home(refresh = true) {
    router.push({name: 'home'}).then(_ => router.go(0));
}

export class Form {
    processing = ref(false);
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
    }

    data() {
        let data = {};

        for (let input of this._inputs) {
            data[input] = this[input];
        }
        return data;
    }

    clearErrors() {
        for (const input of this._inputs) {
            this.errors[input].value = '';
        }
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
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken'),
            },
            mode: 'same-origin',
            body: JSON.stringify(this.data()),
        };
        this.processing.value = true;
        this.clearErrors();

        return fetch(url, options).then(r => this._process(r))
    };

    post(url) {
        return this.submit('POST', url);
    }

    put(url) {
        return this.submit('PUT', url);
    }

    patch(url) {
        return this.submit('PATCH', url);
    }

    delete(url) {
        return this.submit('DELETE', url);
    }

    _process(response) {
        console.assert(response);

        if (response.ok) {
            this._complete();
            return true;
        }

        // console.error(response);
        response.json().then(json => {
            this._processError(json);
            this._complete();
        });
        return false;
    }

    _processError(json) {
        for (const input in json) {
            let error = json[input];

            if (Array.isArray(error)) {
                error = error[0];
            }

            this.setError(input, error);
        }
    }

    _complete() {
        setTimeout(_ => {
            this.processing.value = false;
        }, 1000);
    }
}

export function useForm(data) {
    return new Form(data);
}
