"""USE WHEN NO SPECIFIC COMMAND BOOK"""

from src.common import config, settings, utils
import time
import math
from src.routine.components import Command
from interception import press, key_down, key_up

class Key:
    #Movement
    JUMP = 'space'
    FLASH_JUMP = 'space'
    ROPE_CONNECT = 'x'

    #Buffs
    BUFF_1 = '1'
    BUFF_2 = '2'
    BUFF_3 = '3'
    BUFF_4 = '4'
    BUFF_5 = '5'

    #Skills
    ATTACK_1 = 'a'
    ATTACK_2 = 's'
    ATTACK_3 = 'd'
    ATTACK_4 = 'f'
    ATTACK_5 = 'g'

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
        self.cd30_buff_time = 0
    
    def main(self):
        now = time.time()
        if self.cd30_buff_time == 0 or now - self.cd30_buff_time > 30:
            press(Key.BUFF_1, 2)
            press(Key.BUFF_2, 2)
            press(Key.BUFF_3, 2)
            press(Key.BUFF_4, 2)
            press(Key.BUFF_5, 2)
            self.cd30_buff_time = now


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

class Attack1(Command):
    def main(self):
        press(Key.ATTACK_1, 3)

class Attack2(Command):
    def main(self):
        press(Key.ATTACK_2, 3)

class Attack3(Command):
    def main(self):
        press(Key.ATTACK_3, 3)

class  Attack4(Command):
    def main(self):
        press(Key.ATTACK_4, 3)

class Attack5(Command):
    def main(self):
        press(Key.ATTACK_5, 3)
