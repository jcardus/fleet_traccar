/** @odoo-module **/

import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";

class OdooTraccar extends Component {
    static template = "fleet_traccar.map";

    setup() {
        onWillStart(async () => {
        });
    }
}

registry.category("actions").add("fleet_traccar.map", OdooTraccar);
