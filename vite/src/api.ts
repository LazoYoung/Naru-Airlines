import {reactive, Ref} from "vue";
import router from "@/router/index.js";
import MD5 from "crypto-js/md5.js";

// todo: elevate security measure
export async function fetchProfile(ref: Ref) {
    return fetch("/api/profile/")
        .then((response: Response) => {
            if (!response.ok) {
                ref.value = null;
                return response;
            }

            return response.json()
                .then(json => ref.value = json);
        });
}

export function getGravatarHash(email: string) {
    return MD5(email.trim().toLowerCase());
}

export function getCookie(name: string) {
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
    processing = false;
    errors = {};
    _inputs = [];

    constructor(data: any) {
        let _data = data;

        if (Array.isArray(data)) {
            _data = {};

            for (const element of data) {
                _data[element] = '';
            }
        }

        for (const input in _data) {
            this._inputs.push(input);
            this.errors[input] = '';
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

    clear() {
        this.clearValues();
        this.clearErrors();
    }

    clearValues() {
        for (let input of this._inputs) {
            this[input] = '';
        }
    }

    clearErrors() {
        for (const input of this._inputs) {
            this.errors[input] = '';
        }
    }

    setError(input: string, error: string) {
        if (this.errors.hasOwnProperty(input)) {
            this.errors[input] = error;
        } else {
            alert(error);
        }
    };

    submit(method: string, url: string) {
        let options: RequestInit = {
            method: method,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie('csrftoken'),
            },
            mode: 'same-origin',
            body: JSON.stringify(this.data()),
        };
        this.processing = true;
        this.clearErrors();

        return fetch(url, options).then(r => this._process(r))
    };

    submitPost(url: string) {
        return this.submit('POST', url);
    }

    _process(response: Response) {
        if (response.ok) {
            this._complete();
            return response;
        }

        // console.error(response);
        return response.json().then((json: any) => {
            this._processError(json);
            this._complete();
            return response;
        });
    }

    _processError(json: any) {
        if (typeof json === 'string') {
            this.setError('errors', json);
            return;
        }

        for (const input in json) {
            let error = json[input];

            if (Array.isArray(error)) {
                error = error[0];
            }

            this.setError(input, error);
        }
    }

    _complete() {
        setTimeout(() => {
            this.processing = false;
        }, 1000);
    }
}

export function useForm(data: any): Form {
    let form = new Form(data);
    return reactive(form);
}
