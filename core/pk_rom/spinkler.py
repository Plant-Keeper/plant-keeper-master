import rom


class SprinklerConfig(rom.Model):
    tag = rom.Text(required=True, unique=True)
    soil_moisture_min_level = rom.Float(required=True, default=30)
    soil_moisture_max_level = rom.Float(required=True, default=60)


class SprinklerController(rom.Model):
    tag = rom.Text(required=True, unique=True)
    water_valve_signal = rom.Boolean(default=False)


class Sprinklers:

    def __init__(self):
        self.config = SprinklerConfig
        self.soil_moisture_min_level: float = 0.0
        self.soil_moisture_max_level: float = 0.0

        self.controller = SprinklerController
        self.water_valve_signal: bool = False

    def update_config(
            self,
            tag: str,
            soil_moisture_min_level: float,
            soil_moisture_max_level: float,
    ):
        try:
            self.config \
                .get_by(tag=tag) \
                .update(soil_moisture_min_level=soil_moisture_min_level,
                        soil_moisture_max_level=soil_moisture_max_level) \
                .save()
        except AttributeError:
            self.config(
                tag=tag,
                soil_moisture_min_level=soil_moisture_min_level,
                soil_moisture_max_level=soil_moisture_max_level
            ).save()

    def get_config(self, tag: str):
        c = self.config.get_by(tag=tag)
        self.soil_moisture_min_level = c.soil_moisture_min_level
        self.soil_moisture_max_level = c.soil_moisture_max_level

    def update_controller(
            self,
            tag: str,
            water_valve_signal: bool):
        try:
            self.controller \
                .get_by(tag=tag) \
                .update(water_valve_signal=water_valve_signal) \
                .save()
        except AttributeError:
            self.controller(
                tag=tag,
                water_valve_signal=water_valve_signal
            ).save()

    def is_any_require_water(self) -> bool:
        """
        Check if any of sprinkler required water
        :return:
        """
        for _ in self.controller.query.all():
            if _.water_valve_signal:
                return True
        return False
