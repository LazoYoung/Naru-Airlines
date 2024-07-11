'use strict';

import Animate from "@/animate.js";

/**
 * @license Original source kindly provided by wnynya (https://github.com/wnynya)
 */
class Alert {
    type;
    style;
    timeout;
    notifications;

    /**
     * Instantiate the notification wizard
     * @param type string : rainbow | warn | error | success
     * @param timeout Pop-up duration
     * @param style CSS style mappings
     */
    constructor(type = 'success', style = {}, timeout = 5000) {
        let defStyle = {};
        this.type = type;
        this.style = Object.assign(defStyle, style);
        this.timeout = timeout;
        this.notifications = document.querySelector('#notifications');

        if (!this.notifications) {
            this.notifications = document.createElement('div');
            this.notifications.id = 'notifications';
            const styleElem = document.createElement('style');
            styleElem.innerText = this.getStyle();
            this.notifications.appendChild(styleElem);
            document.body.appendChild(this.notifications);
        }
    }

    /**
     * @param style CSS style mappings
     */
    setStyle(style) {
        this.style = style;
    }

    /**
     * @param timeout set timeout in seconds
     */
    setTimeout(timeout) {
        this.timeout = timeout;
    }

    /**
     * @param type string : rainbow | warn | error | success
     */
    setType(type) {
        this.type = type;
    }

    /**
     * Display the modal.
     * @param message text to display
     */
    pop(message) {
        const notification = document.createElement('div');
        notification.classList.add('notification');

        if (this.type) {
            notification.classList.add(this.type);
        }
        if (this.type === 'rainbow') {
            notification.setAttribute('color', this.type);
        }

        let animate = new Animate(notification);
        let msg = document.createElement('div');
        msg.classList.add('message');
        msg.innerHTML = message;
        let close = document.createElement('div');
        close.classList.add('close');
        let closeBtn = document.createElement('div');
        let ct = setTimeout(() => {
            this.close(animate, notification, null);
        }, this.timeout);
        closeBtn.classList.add('btn');
        closeBtn.innerHTML = '×';
        closeBtn.addEventListener('click', () => {
            this.close(animate, notification, ct);
        });
        close.appendChild(closeBtn);
        notification.appendChild(msg);
        notification.appendChild(close);
        if (this.style) {
            for (const key in this.style) {
                notification.style[key] = this.style[key];
            }
        }
        this.notifications.appendChild(notification);
        setTimeout(() => {
            //notification.classList.add('show');
            animate.spring(0.35, 5).to({right: '0px'}, 1000);
        }, 100);
    }

    /**
     * Close the modal.
     * @param animate Animate node to be cleared
     * @param notification Notification node
     * @param ct closing timer to be cleared
     */
    close(animate, notification, ct) {
        if (ct) {
            clearTimeout(ct);
        }

        notification.classList.add('hide');
        animate.easeout().to({right: '-900px'}, 200);
        setTimeout(() => {
            this.notifications.removeChild(notification);

            if (this.notifications.children.length === 0) {
                document.body.removeChild(this.notifications);
            }
        }, 200);
    }

    getStyle() {
        return `
    #notifications {
      position: fixed;
      display: block;
      z-index: 500000000;
      top: 5rem;
      right: 1rem;
      width: calc(min((100vw - 4rem), 36rem));
      height: calc(100vh - 12rem);
      transition: top 0.2s ease-out, right 0.2s ease-out, max-width 0.2s ease-out;
      pointer-events: none;
      --button-bg: black;
      --button-fg: white;
    }
    #notifications .notification {
      position: relative;
      display: block;
      right: -900px;
      width: max-content;
      max-width: calc(100% - 4rem);
      padding: 1rem 3rem 1rem 1rem;
      margin-bottom: 1rem;
      margin-right: 0px;
      margin-left: auto;
      border-radius: 1rem;
      transition: /*right 0.35s cubic-bezier(0, 0, 0.3, 1.3),*/ opacity 0.2s ease-out, transform 0.2s ease-out,
        max-width 0s ease-out;
      text-align: left;
      box-shadow: 0 0 1rem rgba(0, 0, 0, 0.2);
      pointer-events: all;
    }
    #notifications .notification.show {
      right: 0px;
    }
    #notifications .notification.hide {
      opacity: 0;
      transform: scale(0);
    }
    #notifications .notification {
      background: var(--bg);
      color: var(--fg);
    }
    #notifications .notification.warn,
    #notifications .notification.yellow {
      background: var(--yellow);
      color: var(--t245);
    }
    #notifications .notification.error,
    #notifications .notification.red {
      background: var(--red);
      color: var(--t245);
    }
    #notifications .notification.success,
    #notifications .notification.green {
      background: var(--green);
      color: var(--t245);
    }
    #notifications .notification > .message {
      position: relative;
      display: inline;
      word-break: break-all;
      font-family: var(--sans-serif);
      font-weight: 500;
      font-size: 1rem;
      line-height: 150%;
    }
    #notifications .notification > .close {
      position: absolute;
      display: flex;
      justify-content: center;
      align-items: center;
      top: 0px;
      right: 0.5rem;
      width: 2rem;
      height: 100%;
    }
    #notifications .notification > .close > .btn {
      position: absolute;
      display: flex;
      justify-content: center;
      align-items: center;
      width: 1.5rem;
      height: 1.5rem;
      border-radius: 100%;
      font-family: var(--sans-serif);
      font-weight: 500;
      font-size: 1.25rem;
      background-color: rgba(255,255,255, 0.15);
      cursor: pointer;
    }
    #notifications .notification.rainbow {
      background: linear-gradient(
        to right,
        rgba(255, 0, 0, 1),
        rgba(255, 154, 0, 1),
        rgba(208, 222, 33, 1),
        rgba(79, 220, 74, 1),
        rgba(63, 218, 216, 1),
        rgba(47, 201, 226, 1),
        rgba(28, 127, 238, 1),
        rgba(95, 21, 242, 1),
        rgba(186, 12, 248, 1),
        rgba(251, 7, 217, 1),
        rgba(255, 0, 0, 1),
        rgba(255, 154, 0, 1),
        rgba(208, 222, 33, 1),
        rgba(79, 220, 74, 1),
        rgba(63, 218, 216, 1),
        rgba(47, 201, 226, 1),
        rgba(28, 127, 238, 1),
        rgba(95, 21, 242, 1),
        rgba(186, 12, 248, 1),
        rgba(251, 7, 217, 1),
        rgba(255, 0, 0, 1)
      );
      background-size: 200% 100%;
      color: white;
      animation-name: rainbow;
      animation-duration: 1s;
      animation-timing-function: linear;
      animation-direction: normal;
      animation-iteration-count: infinite;
    }
    @media (max-width: 600px) {
      #notifications {
        top: 4rem;
        right: 1rem;
        max-width: calc(min((100vw - 2rem), 36rem));
        height: calc(100vh - 8rem);
      }
    }`;
    }
}

export default Alert;

window.noty = (...args) => {
    new Alert(...args);
};
