import { reactive, type Ref } from "vue";
import router from "@/router";
import MD5 from "crypto-js/md5";

export class Profile {
    bio = "";
    email = "";
    display_name = "";
    receive_emails = "";
}

// todo: elevate security measure
export async function fetchProfile(ref: Ref<Profile | undefined>) {
    const response = await fetch("/api/profile/");

    if (!response.ok) {
        ref.value = undefined;
        return response;
    }

    if (ref.value == null) {
        ref.value = new Profile();
    }

    const json = await response.json();
    ref.value.bio = json["bio"];
    ref.value.email = json["email"];
    ref.value.display_name = json["display_name"];
    ref.value.receive_emails = json["receive_emails"];
}

export function getGravatarHash(email: string) {
    return MD5(email.trim().toLowerCase());
}

export function getCookie(name: string) {
    const regex = new RegExp(`(^| )${name}=([^;]+)`);
    const match = document.cookie.match(regex);

    if (!match) {
        return null;
    }
    return match[2];
}

export function home(refresh = true) {
    router.push({ name: "home" }).then((_) => router.go(0));
}

export class Form {
    processing = false;
    errors: any = {};
    _inputs: string[] = [];

    constructor(data: any) {
        let _data = data;

        if (Array.isArray(data)) {
            _data = {};

            for (const element of data) {
                _data[element] = "";
            }
        }

        for (const input in _data) {
            this._inputs.push(input);
            this.errors[input] = "";
            this[input] = _data[input];
        }
    }

    data() {
        const data: any = {};

        for (const input of this._inputs) {
            data[input] = this[input];
        }
        return data;
    }

    clear() {
        this.clearValues();
        this.clearErrors();
    }

    clearValues() {
        for (const input of this._inputs) {
            this[input] = "";
        }
    }

    clearErrors() {
        for (const input of this._inputs) {
            this.errors[input] = "";
        }
    }

    setError(input: string, error: string) {
        if (Object.prototype.hasOwnProperty.call(this.errors, input)) {
            this.errors[input] = error;
        } else {
            alert(error);
        }
    }

    async submit(method: string, url: string) {
        const options: RequestInit = {
            method: method,
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken") ?? "",
            },
            mode: "same-origin",
            body: JSON.stringify(this.data()),
        };
        this.processing = true;
        this.clearErrors();

        const response = await fetch(url, options);
        return this._process(response);
    }

    submitPost(url: string) {
        return this.submit("POST", url);
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
        if (typeof json === "string") {
            this.setError("errors", json);
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
    const form = new Form(data);
    return reactive(form);
}
