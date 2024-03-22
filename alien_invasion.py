from power_up_machine_gun import MachineGunPowerUp
from power_up_god_bullet import GodBulletPowerUp
from background import BackGround
from scoreboard import Scoreboard
from game_stats import GameStats
from pygame.sprite import Group
from settings import Settings
from menu_art import MenuArt
import game_functions as gf
from button import Button
from sounds import Sound
from alien import Alien
from ship import Ship
import pygame

# to do: 
# -add getting hit varity
# -adjust game progression
# -add more power_ups
# -fix machine gun mode/ give cooldown
# -add texture to powerup
# -overall polish
# -add more menu options.
# ?add more spice to gameplay


def run_game():
    '''Initialize pygame, Settings and screen object.'''
    pygame.init()
    
    stats = GameStats()
    ai_settings = Settings(stats)
    # Screen object.
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Instances.
    play_button = Button(ai_settings, screen, "Play")
    menu_art = MenuArt(ai_settings, screen, stats)
    sb = Scoreboard(ai_settings, screen, stats)
    bg = BackGround(screen)
    sound = Sound()

    # Groups.
    ship = Ship(ai_settings, screen)
    power_ups = Group()
    bullets = Group()
    aliens = Group()

    # Making initial alien fleet. 
    gf.create_fleet(ai_settings, screen, stats, ship, aliens)

    # equality instances.
    alien = Alien(ai_settings, screen, stats)
    god_bullet_eq_instance = GodBulletPowerUp(ai_settings, screen, stats, alien)
    machine_gun_eq_instance = MachineGunPowerUp(ai_settings, screen, stats, alien)

    # Main game loop.
    while True:

        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, 
                 bullets, sound, power_ups)
        if stats.game_active:
            ship.update()
            gf.update_bullet(ai_settings, screen, stats, sb, ship, aliens, bullets,
                             sound, power_ups)
            gf.update_aliens(ai_settings, stats, sb , screen, ship, aliens, bullets, sound, 
                             power_ups)
            gf.update_power_ups(
                screen.get_rect(), stats, ship, power_ups, god_bullet_eq_instance,
                machine_gun_eq_instance
                )
            gf.end_power(ai_settings, stats, stats.active_powers, god_bullet_eq_instance, 
                         machine_gun_eq_instance)
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                         play_button, sound, menu_art, power_ups, bg)
        gf.update_music(stats, sound)

run_game()
 