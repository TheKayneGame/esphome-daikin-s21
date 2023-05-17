"""
Daikin S21 Mini-Split ESPHome component config validation & code generation.
"""

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import climate
from esphome.const import CONF_ID
from .. import daikin_s21_ns, DaikinS21

CONF_S21_ID = "s21_id"

DaikinS21Climate = daikin_s21_ns.class_("DaikinS21Climate", climate.Climate,
                                        cg.PollingComponent)
uart_ns = cg.esphome_ns.namespace("uart")
UARTComponent = uart_ns.class_("UARTComponent")

CONFIG_SCHEMA = cv.All(
    climate.CLIMATE_SCHEMA.extend(
        {
            cv.GenerateID(): cv.declare_id(DaikinS21Climate),
            cv.GenerateID(CONF_S21_ID): cv.use_id(DaikinS21),
        }
    )
    .extend(cv.polling_component_schema("5s"))
)


async def to_code(config):
    """Generate code"""
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await climate.register_climate(var, config)
    s21_var = await cg.get_variable(config[CONF_S21_ID])
    cg.add(var.set_s21(s21_var))
