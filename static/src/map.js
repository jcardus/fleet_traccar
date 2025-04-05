/** @odoo-module **/

import {Component, onWillStart} from "@odoo/owl"
import {registry} from "@web/core/registry"
import {rpc} from "@web/core/network/rpc";
import {session} from "@web/session";

async function generatePassword(email) {
    const encoder = new TextEncoder();
    const data = encoder.encode(email);
    const hashBuffer = await crypto.subtle.digest('SHA-256', data);
    const hashArray = Array.from(new Uint8Array(hashBuffer));
    return hashArray.map(byte => byte.toString(16).padStart(2, '0')).join('');
}

class OdooTraccar extends Component {
    static template = "fleet_traccar.map"
    setup() {
        this.formData = new URLSearchParams();
        onWillStart(async () => {
            let response = await fetch('/fleet_traccar/api/session')
            if (response.status === 404) {
                await this.setEmailPass(session)
                response = await this.login();
                if (response.status === 401) {
                    await fetch('/fleet_traccar/api/users', {
                        method: "POST",
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({email: this.email, password:this.password, name: this.email}),
                    });
                    await this.login()
                }
            }
        });
    }

    async setEmailPass(session) {
        const instance_id = await rpc('/fleet_traccar/instance_id')
        const company_id = session.user_companies.current_company
        this.email = `odoo${company_id}_${instance_id}@frotaweb.com`;
        this.password = await generatePassword(this.email)
        this.formData.set("email", this.email);
        this.formData.set("password", this.password);
    }
    login = () => fetch('/fleet_traccar/api/session', {
            method: "POST",
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: this.formData
        })

}

registry.category("actions").add("fleet_traccar.map", OdooTraccar);
