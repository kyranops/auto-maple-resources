"""A collection of all commands that Adele can use to interact with the game. 	"""

from src.common import config, settings, utils
import time
import math
from src.routine.components import Command
from interception import press, key_down, key_up

class Key:
    #Movement
    JUMP = 'space'
    FLASH_JUMP = 'space'
    DEMON_STRIKE = 's'
    ROPE_CONNECT = 'x'

    #Buffs
    DEMONIC_FORTITUDE = '3'
    AURA_WEAPON = '['
    CALL_MASTEMA = ']'
    DEMON_GODDESS = 'l'
    RELEASE_OVERLOAD = 'shift'

    #Buffs Toggle
    DEMON_FRENZY = 'end'

    #Skills
    BLOOD_FEAST = 'w'
    SHIELD_CHASING = 'e'
    EXECUTION = 'a'
    MOONLIGHT_SLASH = 'd'
    THOUSAND_SWORDS = 'f'
    SPIDER_IN_THE_MIRROR = ';'
    CREST_OF_THE_SOLAR = '\''
    ERDA_SHOWER = 'c'


#########################
#       Commands        #
#########################
def step(direction, target):
    """
    Performs one movement step in the given DIRECTION towards TARGET.
    Should not press any arrow keys, as those are handled by Auto Maple.
    """

    num_presses = 2
    if direction == 'up' or direction == 'down':
        num_presses = 1
    if config.stage_fright and direction != 'up' and utils.bernoulli(0.75):
        time.sleep(utils.rand_float(0.1, 0.3))
    d_y = target[1] - config.player_pos[1]
    if abs(d_y) > settings.move_tolerance * 1.5:
        if direction == 'down':
            press(Key.JUMP, 3)
        elif direction == 'up':
            press('up', 3)
    press(Key.FLASH_JUMP, num_presses)

class Adjust(Command):
    """Fine-tunes player position using small movements."""

    def __init__(self, x, y, max_steps=5):
        super().__init__(locals())
        self.target = (float(x), float(y))
        self.max_steps = settings.validate_nonnegative_int(max_steps)

    def main(self):
        counter = self.max_steps
        toggle = True
        error = utils.distance(config.player_pos, self.target)
        while config.enabled and counter > 0 and error > settings.adjust_tolerance:
            if toggle:
                d_x = self.target[0] - config.player_pos[0]
                threshold = settings.adjust_tolerance / math.sqrt(2)
                if abs(d_x) > threshold:
                    walk_counter = 0
                    if d_x < 0:
                        key_down('left')
                        while config.enabled and d_x < -1 * threshold and walk_counter < 60:
                            time.sleep(0.05)
                            walk_counter += 1
                            d_x = self.target[0] - config.player_pos[0]
                        key_up('left')
                    else:
                        key_down('right')
                        while config.enabled and d_x > threshold and walk_counter < 60:
                            time.sleep(0.05)
                            walk_counter += 1
                            d_x = self.target[0] - config.player_pos[0]
                        key_up('right')
                    counter -= 1
            else:
                d_y = self.target[1] - config.player_pos[1]
                if abs(d_y) > settings.adjust_tolerance / math.sqrt(2):
                    if d_y < 0:
                        press(Key.ROPE_CONNECT, 1)
                        time.sleep(2)
                    else:
                        key_down('down')
                        press(Key.JUMP, 2)
                        key_up('down')
                    counter -= 1
            error = utils.distance(config.player_pos, self.target)
            toggle = not toggle

class Buff(Command):
    def __init__(self):
        super().__init__(locals())
        self.cd60_buff_time = 0
        self.cd120_buff_time = 0
    
    def main(self):
        buffs = [Key.DEMONIC_FORTITUDE]
        now = time.time()

        if self.cd60_buff_time == 0 or now - self.cd60_buff_time > 60:
            press(Key.DEMONIC_FORTITUDE, 2)
            press(Key.RELEASE_OVERLOAD, 2)
            self.cd60_buff_time = now
        if self.cd120_buff_time == 0 or now - self.cd120_buff_time > 120:
            press(Key.AURA_WEAPON, 2)
            press(Key.CALL_MASTEMA, 2)
            press(Key.DEMON_GODDESS, 2)
            self.cd120_buff_time = now


class FlashJump(Command):
    """Performs a flash jump in the given direction."""

    def __init__(self, direction):
        super().__init__(locals())
        self.direction = settings.validate_arrows(direction)

    def main(self):
        key_down(self.direction)
        time.sleep(0.1)
        press(Key.FLASH_JUMP, 1)
        if self.direction == 'up':
            press('up', 2)
        else:
            press(Key.FLASH_JUMP, 1)
        key_up(self.direction)
        time.sleep(0.5)

class Execution(Command):
    """
    Performs Execution in a given direction
    """
    def __init__(self, direction, attacks=2, repetitions=1):
        super().__init__(locals())
        self.direction = settings.validate_horizontal_arrows(direction)
        self.attacks = int(attacks)
        self.repetitions = int(repetitions)

    def main(self):
        time.sleep(0.05)
        key_down(self.direction)
        time.sleep(0.05)
        if config.stage_fright and utils.bernoulli(0.7):
            time.sleep(utils.rand_float(0.1, 0.3))
        for _ in range(self.repetitions):
            press(Key.EXECUTION, self.attacks, up_time=0.05)
        key_up(self.direction)
        if self.attacks > 2:
            time.sleep(0.3)
        else:
            time.sleep(0.2)

class  MoonlightSlash(Command):
    """
    Uses Moonlight Slash Once
    """
    def main(self):
        press(Key.MOONLIGHT_SLASH, 3)

class BloodFeast(Command):
    """Uses Blood Feast once."""

    def main(self):
        press(Key.BLOOD_FEAST, 3)

class ShieldChasing(Command):
    """Uses Shield Chasing once."""

    def main(self):
        press(Key.SHIELD_CHASING, 3)

class ThousandSwords(Command):
    """Uses Thousand Swords once."""

    def main(self):
        press(Key.THOUSAND_SWORDS, 3)

class SpiderInTheMirror(Command):
    """Uses Spider in the Mirror once"""

    def main(self):
        press(Key.SPIDER_IN_THE_MIRROR, 3)

class CrestOfTheSolar(Command):
    """Uses Crest of the Solar once."""

    def main(self):
        press(Key.CREST_OF_THE_SOLAR, 3)

class ErdaShower(Command):
    """Uses Erda Shower once"""
    
    def main(self):
        key_down("down")
        press(Key.ERDA_SHOWER, 2)
        key_up("down")


