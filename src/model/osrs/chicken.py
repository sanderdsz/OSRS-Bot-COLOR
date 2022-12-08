from model.bot import Bot, BotStatus
from model.runelite_bot import RuneLiteBot
import time
import pyautogui as pag


class Chicken(RuneLiteBot):
    def __init__(self):
        title = "Chicken"
        description = ("Chicken example")
        super().__init__(title=title, description=description)
        self.running_time = 0

    def create_options(self):
        self.options_builder.add_slider_option("running_time", "How long to run (minutes)?", 1, 180)  # max 180 minutes
        self.options_builder.add_checkbox_option("multi_select_example", "Multi-select Example", ["A", "B", "C"])
        self.options_builder.add_dropdown_option("menu_example", "Menu Example", ["A", "B", "C"])

    def save_options(self, options: dict):
        self.options_set = True
        for option in options:
            if option == "running_time":
                self.running_time = options[option]
                self.log_msg(f"Bot will run for {self.running_time} minutes.")
            elif option == "multi_select_example":
                self.multi_select_example = options[option]
                self.log_msg(f"Multi-select example set to: {self.multi_select_example}")
            elif option == "menu_example":
                self.menu_example = options[option]
                self.log_msg(f"Menu example set to: {self.menu_example}")
            else:
                self.log_msg(f"Unknown option: {option}")
                self.options_set = False

        if self.options_set:
            self.log_msg("Options set successfully.")
        else:
            self.log_msg("Failed to set options.")
            print("Developer: ensure option keys are correct, and that the option values are being accessed correctly.")

    def main_loop(self):  # sourcery skip: min-max-identity, switch
        # --- CLIENT SETUP ---
        self.setup_client(window_title="RuneLite", set_layout_fixed=True, logout_runelite=True, collapse_runelite_settings=True)

        # --- RUNTIME PROPERTIES ---
        self.chicken_kills = 0
        feather_inventory = self.inventory_slots[1][1]
        feather_inventory_color = pag.pixel(feather_inventory.x, feather_inventory.y)

        # --- MAIN LOOP ---
        start_time = time.time()
        end_time = 9999999999999999999
        while time.time() - start_time < end_time:
            if not self.status_check_passed():
                return

            #1. Locate chickens
            self.log_msg(f"Looking another chicken at: {time.time()}")
            chicken = self.get_nearest_tag(self.TAG_BLUE)
            if chicken is None:
                time.sleep(3)
                continue

            #3 Click the chicken
            self.mouse.move_to(point=chicken, duration=0.3, destination_variance=3, time_variance=0.001, tween='rand')
            self.mouse.click()

            #4 Kill the chicken
            while self.is_in_combat():
                if not self.status_check_passed():
                    return
                self.log_msg("Killing chicken...")

            #5 Return to the loop
            self.chicken_kills += 1
            self.log_msg(f"Chickens killed: {self.chicken_kills}")
            self.update_progress((time.time() - start_time) / end_time)

        # If the bot reaches here it has completed its running time.
        self.update_progress(1)
        self.log_msg("Bot has completed all of its iterations.")
        self.set_status(BotStatus.STOPPED)
