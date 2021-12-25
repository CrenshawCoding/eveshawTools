# TODO: Create various states for the display model. I.e. Tracking/Appraising, Region: Jita/Amarr, Item Value: Buy/Sell
import enum

import appraiser
import customExceptions
import my_parser
import statisticsModel
import tracker


class Mode(enum.Enum):
    APPRAISAL = 0
    TRACKING = 1


class RegionColorCodes(enum.Enum):
    THE_FORGE = "#298fca"
    DOMAIN = "#f2d600"


class DisplayModel:
    def __init__(self):
        self.mode = Mode.TRACKING
        self.region_to_query = appraiser.Regions.THE_FORGE
        self.order_type = appraiser.OrderType.BUY
        self.statistics_model = statisticsModel.StatisticsModel()
        self.appraiser = appraiser.Appraiser(self.region_to_query)
        self.current_appraisal = None
        self.appraisal_value = 0
        self.number_of_runs = self.statistics_model.number_of_runs
        self.average_loot_per_run = self.statistics_model.average_loot_per_run
        self.switch_mode_button_text = None
        self.switch_region_to_query_button_text = None
        self.switch_region_to_query_button_color = None
        self.switch_order_type_button_text = None
        self.valid_input = True

    def appraise_callback(self, loot_input_raw: str):
        parsed_loot = my_parser.parse_loot(loot_input_raw)
        try:
            self.current_appraisal = self.appraiser.generate_appraisal(parsed_loot)
            self.appraisal_value = self.current_appraisal.total_value
            self.valid_input = True
        except (customExceptions.InputInvalid, customExceptions.ResponseError) as e:
            self.appraisal_value = None
            self.valid_input = False
        self.update_display_model()

    def update_display_model(self):
        if self.valid_input:
            if self.mode == Mode.TRACKING:
                tracker.save_run(self.current_appraisal)
                self.statistics_model.update_statistics()
                self.number_of_runs = self.statistics_model.number_of_runs
                self.average_loot_per_run = self.statistics_model.average_loot_per_run

    def switch_mode_callback(self):
        if self.mode == Mode.TRACKING:
            self.mode = Mode.APPRAISAL
            self.switch_mode_button_text = "Mode: Appraisal"
        else:
            self.mode = Mode.TRACKING
            self.switch_mode_button_text = "Mode: Tracking"

    def switch_region_to_query_callback(self):
        if self.region_to_query == appraiser.Regions.THE_FORGE:
            self.region_to_query = appraiser.Regions.DOMAIN
            self.switch_region_to_query_button_text = "Domain"
            self.switch_region_to_query_button_color = RegionColorCodes.DOMAIN.value
        else:
            self.region_to_query = appraiser.Regions.THE_FORGE
            self.switch_region_to_query_button_text = "The Forge"
            self.switch_region_to_query_button_color = RegionColorCodes.THE_FORGE.value
        self.appraiser = appraiser.Appraiser(region=self.region_to_query, order_type=self.order_type)

    def switch_order_type(self):
        if self.order_type == appraiser.OrderType.BUY:
            self.order_type = appraiser.OrderType.SELL
            self.switch_order_type_button_text = "Sell"
        else:
            self.order_type = appraiser.OrderType.BUY
            self.switch_order_type_button_text = "Buy"
        self.appraiser = appraiser.Appraiser(region=self.region_to_query, order_type=self.order_type)

    def delete_last_run(self):
        tracker.delete_last_run()
