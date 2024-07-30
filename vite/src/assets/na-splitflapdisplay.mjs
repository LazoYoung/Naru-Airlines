export default customElements.define(
    'na-splitflapdisplay',

    class extends HTMLElement {
        constructor() {
            super();
        }

        connectedCallback() {
            const shadow = this.attachShadow({ mode: 'open' });

            const style = document.createElement('style');
            style.textContent = `
                * {
                    box-sizing: border-box;
                    font-family: var(--font-family);
                }
                :host {
                    display: block;
                    width: 100px;
                    height: 200px;
                    position: relative;
                    background: red;
                }
                .top {
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 50%;
                }
                .topText 
            `;
            shadow.appendChild(style);

            const top = document.createElement('div');
            const topText = document.createElement('div');

            top.classList.add('top');
            topText.classList.add('toptext');
            topText.innerHTML = 'A';

            const bottom = document.createElement('div');
            const top2 = document.createElement('div');
            const bottom2 = document.createElement('div');

            shadow.appendChild(top);
            shadow.appendChild(bottom);
            shadow.appendChild(top2);
            shadow.appendChild(bottom2);
        }

        disconnectedCallback() {}

        adoptedCallback() {}

        static observedAttributes = ['value'];

        get value() {
            return 'a';
        }

        set value(newValue) {
            if (newValue) {
                this.setAttribute('value', newValue);
            } else {
                this.removeAttribute('value');
            }
        }

        attributeChangedCallback(name, oldValue, newValue) {
            if (oldValue == newValue) {
                return;
            }
            if (this[name]) {
                this[name] = newValue;
            }
        }
    }
);
