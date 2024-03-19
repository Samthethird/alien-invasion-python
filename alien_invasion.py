from power_up_machine_gun import MachineGunPowerUp
from power_up_god_bullet import GodBulletPowerUp
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


def run_game():
    '''Initialize pygame, Settings and screen object.'''
    pygame.init()
    pygame.mixer.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Make the play button.
    play_button = Button(ai_settings, screen, "Play")

    # Create an instance to store the games statistics and scoreboard
    # Handle sounds and Menu Art aswell.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)
    sound = Sound()
    menu_art = MenuArt(ai_settings, screen)

    # Make a group for power_ups .
    power_ups = Group()

    # Make a ship, a group for bullets and aliens.
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    # Making a fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens)

    # equality instances.
    alien = Alien(ai_settings, screen)
    god_bullet_eq_instance = GodBulletPowerUp(ai_settings, screen, stats, alien)
    machine_gun_eq_instance = MachineGunPowerUp(ai_settings, screen, stats, alien)

    # Main loop for the game.
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
                         play_button, sound, menu_art, power_ups)
        gf.update_music(stats, sound)
run_game()
 