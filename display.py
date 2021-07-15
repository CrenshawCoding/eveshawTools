import tkinter
import tkinter.messagebox

import customExceptions
import displayModel


class Display:

    # TODO: Seperate tracking from appraising. Create 2 modes: 1 where appraising auto tracks, one where it doesn't
    def appraise_callback(self):
        try:
            self.display_model.appraise_callback(self.appraisal_input.get(1.0, "end-1c"))
            self.appraisal_input.delete(1.0, "end")
            self.update_display()
            # TODO: update texts im model
        except customExceptions.ResponseError:
            print("Input Invalid")
            self.currrent_appraisal_value_text.set("Invalid Input")

    def switch_mode_callback(self):
        self.display_model.switch_mode_callback()
        self.switch_mode_button["text"] = self.display_model.switch_mode_button_text
        self.update_layout()

    def switch_region_to_query_callback(self):
        self.display_model.switch_region_to_query_callback()
        self.switch_region_to_query_button["text"] = self.display_model.switch_region_to_query_button_text
        self.switch_region_to_query_button["bg"] = self.display_model.switch_region_to_query_button_color
        self.update_display()

    def switch_order_type_callback(self):
        self.display_model.switch_order_type()
        self.switch_order_type_button["text"] = self.display_model.switch_order_type_button_text
        self.update_display()

    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Abyssal Loot Tracker and Appraiser")
        self.display_model = displayModel.DisplayModel()
        self.currrent_appraisal_value_text = tkinter.StringVar()
        self.statistics_display_text = tkinter.StringVar()
        self.region_to_query_display_text = tkinter.StringVar()
        self.appraisal_input = tkinter.Text(self.root, height=10, width=30)
        self.current_run_loot_value_label = tkinter.Label(self.root, textvariable=self.currrent_appraisal_value_text)
        self.statistics_label = tkinter.Label(self.root, textvariable=self.statistics_display_text, justify="left")
        self.appraise_button = tkinter.Button(self.root, text="Appraise", command=self.appraise_callback)
        self.switch_mode_button = tkinter.Button(self.root, text="Mode: Tracking", command=self.switch_mode_callback)
        self.switch_region_to_query_button = tkinter.Button(self.root, text="Jita",
                                                            command=self.switch_region_to_query_callback,
                                                            bg=displayModel.RegionColorCodes.THE_FORGE.value)
        self.switch_order_type_button = tkinter.Button(self.root, text="Buy", command=self.switch_order_type_callback)
        self.update_display()
        self.update_layout()

    def update_layout(self):
        self.appraisal_input.grid(column=0, row=1)
        self.current_run_loot_value_label.grid(column=0, row=2, sticky="w")
        self.appraise_button.grid(column=0, row=0)
        self.switch_mode_button.grid(column=1, row=0)
        self.switch_order_type_button.grid(column=0, row=0, sticky="w")
        self.switch_region_to_query_button.grid(column=0, row=0, sticky="e")
        if self.display_model.mode == displayModel.Mode.TRACKING:
            self.statistics_label.grid(column=1, row=1, sticky="nw")
        else:
            self.statistics_label.grid_forget()

    def update_display(self):
        if self.display_model.mode == displayModel.Mode.TRACKING:
            self.statistics_display_text.set("Number of Runs: {0}\nAverage Loot per Run: {1:,}".format(
                self.display_model.number_of_runs,
                self.display_model.average_loot_per_run))
        self.currrent_appraisal_value_text.set("Appraisal Value: {:,}".format(self.display_model.appraisal_value) +
                                               " ISK")

    @staticmethod
    def run():
        tkinter.mainloop()
