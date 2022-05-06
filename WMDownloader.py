# Main logic for importing Weather Underground PWS data and adding it to the Weather Manager database.
# Will import all observations not yet downloaded up until yesterday's date.

class MainRoutine:

    def __init__(self):
        pass

    def download_recent_observations(self):

        most_recent_observation_date = get_most_recent_observation_date()

        # Weather Underground not recording today warner
        # Fetch most recent observation date from database
        # Fetch the latest observations
        # Save the latest observations

        pass

    def get_most_recent_observation_date(self):
        pass

# Dependency factory

# Logger
# WU API
# Database ERM
# Run time parameters
# SMTP client
# Date / Time provider (so that these can be faked)

# Instance and run the main routine


_main_routine = MainRoutine()
_main_routine.download_recent_observations()
