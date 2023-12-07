
from grupprum import Boka_Grupprum

preferences = []

schedule = {
        0:[],                        # Monday
        1:[],                        # Tuesday
        2:[],                        # Wednesday
        3:[],                        # Thursday
        4:[],                        # Friday
        }

# Enter users as nested lists
users = []

Boka_Grupprum(preferences, schedule, users, decode=True)
