from will.plugin import WillPlugin
from will.decorators import respond_to, periodic, hear, randomly, route, rendered_template, require_settings
import random

tmp_room_name_parts=["bacon", "monkey", "foot", "cheese", "hair", "goat",
                     "shoe", "armpit", "karate", "dropkick", "battleship",
                     "trash-on-lawn-in-net"]

class HangoutPlugin(WillPlugin):
    @respond_to("^hangout ?(?P<room>.*)")
    def create_hangout(self, message, room=""):
        room = room.strip()

        if not room:
            # generate a new name
            room = random.choice(tmp_room_name_parts) +  "-" + random.choice(tmp_room_name_parts) + str(random.randint(1, 100))


        url = "https://plus.google.com/hangouts/_/datastax.com/%s?authuser=1" % room

        self.reply(message, "Here's a hangout (%s): %s" % (room, url))

