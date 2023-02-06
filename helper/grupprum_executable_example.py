
"""This is an example of how grupprum_executable.py should look like """


from grupprum import Boka_Grupprum

preferences = [
        "m1212A", 
        "m1212B", 
        "m1212C", 
        "m1212D", 
        "m1212E",
        "m1212F", 
        "m1206B",
        "m1203A",
        "m1215B",
        "m1215A",
        ]

schedule = {
        0:[['08:00','12:00'],['12:30','16:30']],                        # Monday
        1:[['08:00','10:00'],['13:00','17:00']],                        # Tuesday
        2:[['08:00','12:00'],['13:00','17:00']],                        # Wednesday
        3:[['08:00','12:00']],                                          # Thursday
        4:[['08:00','10:00'],['13:00','17:00']],                        # Friday
        }

# Enter users as nested lists, works with one or several users
users = [                        
        ["cid1@net.chalmers.se",b'woiejfoiweiuiiiWiioniWIUOWEOINOIRioiooinDIDD89676779/67697677998__HbigyguUTYUtvyuvyuV-IUIUiugyg=='],
        ["cid2@net.chalmers.se", b'kwqneofiufhiohiuIUHHUHHUUUctyytrctrxcrre454e4645465CTRCXTCTCCRTXR676r547___78687yGTGTFYTFT=='],
        ]

Boka_Grupprum(preferences, schedule, users)