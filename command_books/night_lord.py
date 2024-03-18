from src.common import config, settings, utils
import time
from src.routine.components import Command
from interception import press, key_down, key_up
import math

IMAGE_DIR = config.RESOURCES_DIR + '/command_books/night_lord/'

# List of key mappings
class Key:    
    # Movement
    FLASH_JUMP = 'space'
    JUMP = 'space'
    ROPE = '`'
    UP_JUMP = 'c'
    DASH = 'x' # Shadow Rush

    # Buffs
    Bleeding_Toxin = 'f1' # Bleeding Toxin
    Maple_World_Goddess = 'f2' # Maple World Goddess Blessing
    Explosive_Shuriken = 'f3' # Explosive Shuriken
    Spread_Throw = 'f4' # Spread Throw
    Ultimate_Dark_Sight = '5' # Ultimate Dark Sight
    Blood_for_Blood = 'f5' # Blood for Blood
    Epic_Adventure = 'f6' # Epic Adventure

    # Buffs Toggle

    # Attack Skills
    Showdown_Challenge = 'a' # Showdown Challenge
    Dark_Lords_Secret_Scroll = '1' # Dark Lords Secret Scroll
    Dark_Flare = 'd' # Dark Flare
    Fuma_Shuriken = 's'# Fuma Shuriken
    Sudden_Raid = 'w' # Sudden Raid
    Four_Seasons_Hotel = 'e' # Four Seasons
    Spider_In_The_Mirror = '2' # Spider in the Mirror
    Solar_Crest = '3' # Solar Crest
    Erda_Fountain = '4' # Erda Fountain

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
            press(Key.ROPE, 1)
    press(Key.FLASH_JUMP, num_presses)


class Adjust(Command):

    def __init__(self, x, y, max_steps=8):
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
                            time.sleep(0.02)
                            walk_counter += 1
                            d_x = self.target[0] - config.player_pos[0]
                        key_up('left')
                    else:
                        key_down('right')
                        while config.enabled and d_x > threshold and walk_counter < 60:
                            time.sleep(0.02)
                            walk_counter += 1
                            d_x = self.target[0] - config.player_pos[0]
                        key_up('right')
                    time.sleep(0.1)
                    counter -= 1
            else:
                time.sleep(0.5)
                d_y = self.target[1] - config.player_pos[1]
                if abs(d_y) > settings.adjust_tolerance / math.sqrt(2):
                    if d_y < 0:
                        press(Key.ROPE, 1)
                        time.sleep(1)
                    else:
                        key_down('down')
                        press(Key.JUMP, 2)
                        key_up('down')
                    counter -= 1
                time.sleep(0.1)
            error = utils.distance(config.player_pos, self.target)
            toggle = not toggle


class Buff(Command):
    """Uses each of Nightlord's buffs once."""

    def __init__(self):
        super().__init__(locals())
        self.cd120_buff_time = 0
        self.cd150_buff_time = 0
        self.cd180_buff_time = 0
        self.cd200_buff_time = 0
        self.cd240_buff_time = 0
        self.cd900_buff_time = 0
        self.decent_buff_time = 0

    def main(self):
        now = time.time()
        if self.cd120_buff_time == 0 or now - self.cd120_buff_time > 121:
            press(Key.Blood_for_Blood)
            press(Key.Epic_Adventure)
            self.cd120_buff_time = now
        if self.cd180_buff_time == 0 or now - self.cd150_buff_time > 151:
            self.cd150_buff_time = now
        if self.cd180_buff_time == 0 or now - self.cd180_buff_time > 181:
            press(Key.Maple_World_Goddess)
            press(Key.Bleeding_Toxin)
            press(Key.Explosive_Shuriken)
            press(Key.Spread_Throw)
            self.cd180_buff_time = now
        if self.cd200_buff_time == 0 or now - self.cd200_buff_time > 200:
            self.cd200_buff_time = now
        if self.cd240_buff_time == 0 or now - self.cd240_buff_time > 240:
            self.cd240_buff_time = now
        if self.cd900_buff_time == 0 or now - self.cd900_buff_time > 900:
            self.cd900_buff_time = now

class FlashJump(Command):
    """Performs a flash jump in the given direction."""
    _display_name = 'Flash Jump  '

    def __init__(self, direction="",jump='false',combo='False',triple_jump="False",fast_jump="false",reverse_triple='false'):
        super().__init__(locals())
        self.direction = settings.validate_arrows(direction)
        self.triple_jump = settings.validate_boolean(triple_jump)
        self.fast_jump = settings.validate_boolean(fast_jump)
        self.jump = settings.validate_boolean(jump)
        self.reverse_triple = settings.validate_boolean(reverse_triple)

    def main(self):
        if not self.jump:
            utils.wait_for_is_standing()
            if not self.fast_jump:
                self.player_jump(self.direction)
                time.sleep(utils.rand_float(0.02, 0.04)) # fast flash jump gap
            else:
                key_down(self.direction,down_time=0.05)
                press(config.bot.config['Jump'],down_time=0.06,up_time=0.05)
        else:
            key_down(self.direction,down_time=0.05)
            press(config.bot.config['Jump'],down_time=0.06,up_time=0.05)
        
        press(Key.FLASH_JUMP, 1,down_time=0.06,up_time=0.01)
        key_up(self.direction,up_time=0.01)
        if self.triple_jump:
            time.sleep(utils.rand_float(0.03, 0.05))
            # reverse_direction
            reverse_direction = ''
            if self.reverse_triple:
                if self.direction == 'left':
                    reverse_direction = 'right'
                elif self.direction == 'right':
                    reverse_direction = 'left'
                print('reverse_direction : ',reverse_direction)
                key_down(reverse_direction,down_time=0.05)
            else:
                time.sleep(utils.rand_float(0.02, 0.03))
            press(Key.FLASH_JUMP, 1,down_time=0.07,up_time=0.04) # if this job can do triple jump
            if self.reverse_triple:
                key_up(reverse_direction,up_time=0.01)
        time.sleep(utils.rand_float(0.01, 0.02))

class UpJump(Command):
    """Performs a up jump in the given direction."""
    _display_name = 'Up Jump'
    _distance = 27
    key=Key.UP_JUMP
    delay=0.45
    rep_interval=0.5
    skill_cool_down=0
    ground_skill=False
    buff_time=0
    combo_delay = 0.45

    # def __init__(self,jump='false', direction='',combo='true'):
    #     super().__init__(locals())
    #     self.direction = settings.validate_arrows(direction)

    # def main(self):
    #     utils.wait_for_is_standing(500)
    #     press(Key.UP_JUMP, 1)
    #     key_down(self.direction)
    #     time.sleep(utils.rand_float(0.35, 0.4))
    #     if 'left' in self.direction or 'right' in self.direction:
    #         press(config.bot.config['Jump'], 1)
    #     key_up(self.direction)
        
class Rope(Command):
    """Performs a up jump in the given direction."""
    def main(self):
        press(Key.ROPE, 2)

class Dash(Command):
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
            press(Key.DASH, self.attacks, up_time=0.05)
        key_up(self.direction)
        if self.attacks > 2:
            time.sleep(0.3)
        else:
            time.sleep(0.2)

class Showdown_Challenge(Command):
    def main(self):
        press(Key.Showdown_Challenge, 3)

class Dark_Lords_Secret_Scroll(Command):
    def main(self):
        press(Key.Dark_Lords_Secret_Scroll, 1)

class Dark_Flare(Command):
    def main(self):
        press(Key.Dark_Flare, 1)

class Fuma_Shuriken(Command):
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
            press(Key.Fuma_Shuriken, self.attacks)
        key_up(self.direction)
        if self.attacks > 2:
            time.sleep(0.3)
        else:
            time.sleep(0.2)

class Sudden_Raid(Command):
    def main(self):
        press(Key.Sudden_Raid, 1)

class Four_Seasons_Hotel(Command):
    def main(self):
        press(Key.Four_Seasons_Hotel, 1)

class Spider_In_The_Mirror(Command):
    def main(self):
        press(Key.Spider_In_The_Mirror, 1)

class Solar_Crest(Command):
    def main(self):
        press(Key.Solar_Crest, 1)

class Bleeding_Toxin(Command):
    def main(self):
        press(Key.Bleeding_Toxin, 2)

class Maple_World_Goddess(Command):
    def main(self):
        press(Key.Maple_World_Goddess, 2)

class Explosive_Shuriken(Command):
    def main(self):
        press(Key.Explosive_Shuriken, 2)

class Spread_Throw(Command):
    def main(self):
        press(Key.Spread_Throw, 2)

class Ultimate_Dark_Sight(Command):
    def main(self):
        press(Key.Ultimate_Dark_Sight, 2)

class Blood_for_Blood(Command):
    def main(self):
        press(Key.Blood_for_Blood, 2)

class Epic_Adventure(Command):
    def main(self):
        press(Key.Epic_Adventure, 2)

class Erda_Fountain(Command):
    def main(self):
        key_down("down")
        press(Key.Erda_Fountain, 2)
        key_up("down")
