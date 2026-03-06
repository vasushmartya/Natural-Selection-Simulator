from traits.trait import Trait
from config import Config

# Initialize a default config to base traits on
_default_config = Config()

TRAITS = {
    "speed": Trait("speed", "S", _default_config.high_speed, _default_config.low_speed),
    "vision": Trait("vision", "V", _default_config.high_vision, _default_config.low_vision),
    "attractiveness": Trait("attractiveness", "A", _default_config.dominant_attractive_chance, _default_config.recessive_attractive_chance),
    "violence": Trait("violence", "K", _default_config.more_violent, _default_config.less_violent)
}