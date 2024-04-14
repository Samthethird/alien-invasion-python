from power_up_machine_gun import MachineGunPowerUp
from power_up_god_bullet import GodBulletPowerUp
from power_up_mantis_god import MantisGodPowerUp
from power_up_mantis import MantisPowerUp
from bullet import Bullet
from pathlib import Path
from alien import Alien
from time import sleep
from ship import Ship
import random
import pygame
import json
import sys


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets, sound):
    '''Respond to keyboard and mouse activity.'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_game(stats, sound)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship,
                                 aliens, bullets, sound)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, stats, ship) 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                              bullets, mouse_x, mouse_y, sound)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, 
                      bullets, mouse_x, mouse_y, sound):
    '''Start the game when the player hits the play button.'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets, sound)
        stats.game_counter += 1


def check_keyup_events(event, stats, ship):
    '''Respond to key releases.'''
    if event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_a:
        ship.moving_left = False
    elif event.key == pygame.K_SPACE and stats.machine_gun_active:
        stats.shooting = False


def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, 
                         bullets, sound):
    '''Respond to key presses.'''
    if event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE and not stats.machine_gun_active:
        fire_bullet(ai_settings, screen, stats, ship, bullets, sound)
    elif event.key == pygame.K_SPACE and stats.machine_gun_active:
        stats.shooting = True
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets, sound)


def check_machine_gun_mode(ai_settings, screen, stats, ship, bullets, sound, 
                           ):
    machine_gun_backup(ai_settings, stats)
    now = pygame.time.get_ticks()
    if stats.shooting:
        if stats.god_bullet_active:
            if now - stats.start_time >= 380:
                fire_bullet(ai_settings, screen, stats, ship, bullets, sound, 
                        )
        elif now - stats.start_time >= 200:
            fire_bullet(ai_settings, screen, stats, ship, bullets, sound, 
                        )
                
            
def machine_gun_backup(ai_settings, stats):
    if not stats.machine_gun_active and stats.shooting:
        stats.shooting = False

    if stats.machine_gun_active and ai_settings.bullets_allowed == 3:
        ai_settings.bullets_allowed = 1000


def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets, sound):
    save_game(stats, sound)
    if not stats.game_active:        
        # Reset the games settings.
        ai_settings.initialize_dynamic_settings()

        # Reset music playing state.
        stats.reset_music()

        # Hide mouse cursor.
        pygame.mouse.set_visible(False)

        # Reset the games statistics.
        stats.reset_stats()
        stats.game_active = True

        # Reset scoreboard images.
        sb.prep_images()

        # Empty aliens and bullets.
        aliens.empty()
        bullets.empty()

        stats.active_powers.empty()
        # Create new fleet and center ship.
        create_fleet(ai_settings, screen, stats, ship, aliens)
        ship.center_ship()


def update_screen(screen, stats, sb, ship, aliens, bullets,
                  play_button, sound, menu_art, power_ups, bg, particle_system,
                  health_drops,
                  ):
    '''Update the images on screen and flip to a new screen.'''
    # Redraw the screen during each pass through the loop.
    bg.blitme()

    if stats.game_active:
        # Redraw all the bullets behind ship and alliens.
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        
        particle_system.draw(screen)

        ship.blitme()
        aliens.draw(screen)
        
        # draw each power_up currently on screen.
        if power_ups:
            for power_up in power_ups.sprites():
                power_up.blitme()
        
        if health_drops:
            for drop in health_drops.sprites():
                drop.blitme()

    # Draw the play button and the menu if the game is inactive.
    elif not stats.game_active:
        play_button.draw_button()

        # Draw the main menu.
        menu_art.create_menu_art()
        display_menu_achivement(stats, sb, sound)
        
    # Draw score information.
    sb.show_score()

    # Draw hints
    if stats.hint_activated and not stats.hint_run:
        sb.draw_hint()

    
    # Display the most recent screen.
    pygame.display.flip()

    if not stats.hint_run and stats.hint_activated:
        pygame.time.wait(2500)
        stats.hint_run = True


def display_menu_achivement(stats, sb, sound):
    '''display achivement and game ending sound-effect.'''
    if not stats.game_active:
        sb.prep_achivement()
        sb.draw_achivement()

        if  stats.game_over_s and stats.high_score_beat:
            # Initiate winning audio.
            sound.high_score_beat()

        elif stats.game_over_s:
            # Initiate losing audio.
            sound.high_score_not_beat()

        # set sound to played.
        stats.game_over_s = False


def check_particles(ai_settings, particle_system, bullets, stats, power_ups, 
                    health_drops):
    check_god_bullet_particles(ai_settings, stats, bullets, particle_system)
    check_power_up_particles(power_ups, particle_system, health_drops)
    particle_system.update()


def check_power_up_particles(power_ups, particle_system, health_drops):
    if power_ups:
        for powerup in power_ups:
            particle_system.add_particle(
                powerup.rect.x + powerup.rect.width //2,
                powerup.rect.y + powerup.rect.height,
                (187, 165, 61), dx=(-0.7, 0.7), dy=(-1, 0.3),
                life_time=90, size=3 # 100
            )

    if health_drops:
        for drop in health_drops:
                particle_system.add_particle(
                drop.rect.x + drop.rect.width //2,
                drop.rect.y + drop.rect.height,
                (255, 36, 0), dx=(-0.7, 0.7), dy=(-1, 0.3),
                life_time=90, size=2 # 100
            )


def check_god_bullet_particles(ai_settings, stats, bullets, particle_system):
    if stats.god_bullet_active:
        for bullet in bullets:
            particle_system.add_particle(
                                        bullet.rect.x,
                                        bullet.rect.y + bullet.rect.height // 2,
                                        ai_settings.god_bullet_color,
                                        dx=(-1.4, 1.4), dy=(-0.3, 2), 
                                        life_time=49, size=3 # 51
                                        )
            
            particle_system.add_particle(
                                        bullet.rect.x + bullet.rect.width,
                                        bullet.rect.y + bullet.rect.height // 2,
                                        ai_settings.god_bullet_color,
                                        dx=(-1.4, 1.4), dy=(-0.3, 2), 
                                        life_time=49, size=3
                                        )


def fire_bullet(ai_settings, screen, stats, ship, bullets, sound,
                ):
    '''Make a bullet if limit not reached.'''
    soundb = False
    # mantis mode
    if stats.mantis_active:
        if len(bullets) < ai_settings.bullets_allowed:
            for i in range(1, 3):
                new_bullet = Bullet(ai_settings, screen, ship, stats)
                new_bullet.index = i
                new_bullet.set_location()
                bullets.add(new_bullet)
                soundb = True
                
    # mantis Gode mode
    elif stats.mantis_god_active:
        if len(bullets) < ai_settings.bullets_allowed:
            for i in range(1, 4):
                new_bullet = Bullet(ai_settings, screen, ship, stats)
                new_bullet.index = i
                bullets.add(new_bullet)
                soundb = True
    else:    
        # Create a bullet and add it to the bullets group.
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship, stats)
            bullets.add(new_bullet)
            soundb = True

    #initiate sound effect and particles.
    if stats.game_active and soundb:
        if stats.god_bullet_active:
            sound.fire_god_bullet()
        else:
            sound.fire_bullet()

    stats.start_time = pygame.time.get_ticks()


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets, sound, power_ups):
    '''
    Check if any alien has reached an edge then change
    fleet direction, and check for bottom and ship collisions.
    '''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Detecting ship-alien collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, sound, power_ups)
    
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets, sound, power_ups)


def check_fleet_edges(ai_settings, aliens):
    '''Respond appropriately if any aliens have reached an edge.'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings:object, aliens:object) -> int:
    '''Drop the entire fleet and change directions.'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets, sound, power_ups):
    '''Check for any aliens that reached the bottom of the screen.'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            '''Respond as if the ship is hit.'''
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, sound, power_ups)
            break


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, sound, power_ups):
    '''Respond properly if the ship is hit.'''
    if stats.ships_left > 1:
        next_life(ai_settings, stats, sb, screen, ship, aliens, bullets, sound, power_ups)
    else:
        end_game(stats, sound, power_ups, ai_settings, sb)


def end_game(stats, sound, power_ups, ai_settings, sb):
    save_game(stats, sound)
    sb.prep_high_scores()
    # Initiate hit audio.
    
    sound.ship_hit()

    # pause, finish game, activate gameover sound and make cursor visable.
    sleep(0.5)
    stats.game_active = False
    stats.game_over_s = True
    
    # Reset music played.
    stats.reset_music()
    pygame.mouse.set_visible(True)

    # Rest power_ups.
    power_ups.empty()
    stats.active_powers.empty() 
    ai_settings.reset_god_bullet_settings()


def next_life(ai_settings, stats, sb, screen, ship, aliens, bullets, sound, power_ups):
    '''go to next ship and reset level'''
    # initiate hit audio
    sound.ship_hit()

    # Decrement ships left.
    stats.ships_left -= 1

    # Update scoreboard ships
    sb.prep_ships()

    # Empty the groups of aliens and bullets.
    aliens.empty()
    bullets.empty()
    
    # powers
    ai_settings.reset_god_bullet_settings()
    power_ups.empty()

    # Create new fleet and and center ship.
    check_level(ai_settings, stats)
    create_fleet(ai_settings, screen, stats, ship, aliens)
    ship.center_ship()

    # Pause.
    sleep(0.5)


def update_bullet(ai_settings, screen, stats, sb, ship, aliens, bullets, sound, 
                  power_ups, hit, health_drops):
    '''Update position of bullets and remove old ones and check for alien bullet collisisons.'''
    if stats.mantis_god_active:
        for bullet in bullets:
            bullet.update_mantis_god_mode()
    else:
        # Update bullet positions
        bullets.update()
    
    # Deleting unececary bullets.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, bullets,
                                   aliens, sound, power_ups, hit, health_drops)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, bullets, 
                                  aliens, sound, power_ups, hit, health_drops):
    '''Respond to bullet/alien collisions.'''

    if stats.hard_mode or stats.insane_mode:
        ai_settings.alien_destruction = False
    else:
        ai_settings.alien_destruction = True

    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, ai_settings.bullet_destruction, 
                                            ai_settings.alien_destruction)
    
    hard_mode_collisions(stats, aliens, collisions, hit)

    # increase score if alien hit.
    add_score(ai_settings, stats, sb, collisions, sound)

    # randomly drop a powerup if an alien is killed.
    drop_power_up(ai_settings, screen, stats, power_ups, collisions, health_drops)
    
    next_level(ai_settings, screen, stats, sb, ship, bullets, aliens, sound,
               power_ups)


def next_level(ai_settings, screen, stats, sb, ship, bullets, aliens, sound,
               power_ups):
        if len(aliens) == 0 and stats.level == 5 and not stats.power_up_level_passed:
            power_up_level(ai_settings, screen, stats, sb, ship, sound, bullets, 
                   power_ups, aliens)
        
        elif len(aliens) == 0 and stats.level == 13 and not stats.power_up_level_passed:
            power_up_level(ai_settings, screen, stats, sb, ship, sound, bullets, 
                   power_ups, aliens)

        elif len(aliens) == 0:
            '''proceed to the next level.'''
            # initate next level sound effect.
            sound.next_level()
            # Increase and show level.
            stats.level += 1
            sb.prep_level()

            # Empty bullets.
            bullets.empty()
            ai_settings.increase_alien_worth()
            
            # check level and create fleet
            check_level(ai_settings, stats)
            create_fleet(ai_settings, screen, stats, ship, aliens)

        if stats.level == 12 and stats.power_up_level:
            stats.reset_power_up_level()


def power_up_level(ai_settings, screen, stats, sb, ship, sound, bullets, 
                   power_ups, aliens):
    '''a level, specific for getting a permenant level ups.'''
    # activate events, only once.
    if not stats.power_up_level:
        power_up_level_events(sound, bullets, power_ups, ai_settings, screen, stats)

    # get the time when player got the falling power_up, only once.
    # for mantis mode
    if stats.mantis_active and not stats.one_timeM and stats.level == 5:
        stats.start_timeM = pygame.time.get_ticks()
        stats.one_timeM = True

    # for mantis god mode
    elif stats.mantis_god_active and not stats.one_timeM:
        stats.start_timeM = pygame.time.get_ticks()
        stats.one_timeM = True

    elif not stats.permanent_powers and not stats.one_timeM and not power_ups:
        stats.start_timeM = pygame.time.get_ticks()
        stats.one_timeM = True

    # if playr got power up, start timer and wait one second before going to next level
    if stats.start_timeM > 0:
        now = pygame.time.get_ticks()
        if now - stats.start_timeM >= 1000:
            stats.power_up_level_passed = True
            next_level(ai_settings, screen, stats, sb, ship, bullets, aliens, sound,
                power_ups)
    
    # activate power_Up_level so the things that are meant to happen once dont 
    # happen again
    stats.power_up_level = True
    

def power_up_level_events(sound, bullets, power_ups, ai_settings, screen, stats):
        sound.next_level()
        bullets.empty()
        power_ups.empty()
        # generate power_Up
        if stats.level == 5:
            permanent_power_up = MantisPowerUp(ai_settings, screen, stats)
        else:
            permanent_power_up = MantisGodPowerUp(ai_settings, screen, stats)
        # add to list of permenant power_ups:
        power_ups.add(permanent_power_up)


def hard_mode_collisions(stats, g_aliens, collisions, hit):
    # reducing hp and removeing hard aliens
    if stats.hard_mode or stats.insane_mode:
        if collisions:
            for aliens in collisions.values():
                for alien in aliens:
                    alien.hp -= 1
                    if stats.hard_mode:
                        hit.hard_alien_hit(alien)
                    elif stats.insane_mode:
                        hit.insane_alien_hit(alien)
                    if alien.hp == 0:
                        g_aliens.remove(alien)


def drop_power_up(ai_settings, screen, stats, power_ups, collisions, health_drops):
    '''Randomly drop a powerup when an alien is killed.'''
    if collisions:
        chance = roll_die(stats)

        if chance == 1:
            drop_god_bullet(ai_settings, screen, stats, power_ups, collisions)

        if chance == 2:
            drop_machine_gun(ai_settings, screen, stats, power_ups, collisions)
        
        if chance == 3:
            drop_health(ai_settings, screen, stats, collisions, health_drops)


def drop_health(ai_settings, screen, stats, collisions, health_drops):
    if stats.ships_left < 3 and not health_drops:
        for aliens in collisions.values():
            for alien in aliens:
                health_drop = Ship(ai_settings, screen)

                # set location under the alien.
                health_drop.rect.center = alien.rect.center
                health_drops.add(health_drop)


def drop_god_bullet(ai_settings, screen, stats, power_ups, collisions):
    # drop god_bullet.
    nom = check_one_god_bullet(power_ups)
    if nom < 1:
        for aliens in collisions.values():
            for alien in aliens:
                god_bullet_power_up = GodBulletPowerUp(ai_settings, screen, stats, alien)
                # add it to the power_ups on screen, group.
                power_ups.add(god_bullet_power_up)


def drop_machine_gun(ai_settings, screen, stats, power_ups, collisions):
    # if dice rolled 2 drop a "mahcine_gun" powerup.
    nom = check_one_machine_gun(power_ups)
    if nom < 1:
        for aliens in collisions.values():
            for alien in aliens:
                machine_gun_power_up = MachineGunPowerUp(ai_settings, screen, stats, alien)
                # add it to the power_ups on screen. 
                power_ups.add(machine_gun_power_up)


def check_one_god_bullet(power_ups):
    god_in_power = 0
    for power in power_ups:
        if isinstance(power, GodBulletPowerUp):
            god_in_power += 1
    return god_in_power


def check_one_machine_gun(power_ups):
    machine_in_power = 0
    for power in power_ups:
        if isinstance(power, MachineGunPowerUp):
            machine_in_power += 1
    return machine_in_power


def roll_die(stats):
    #roll a dice to determine power_up dropped.
    if stats.level < 6:
        chance = random.randint(1, 200)
    elif stats.level < 13:
        chance = random.randint(1, 170)
    elif stats.level < 18:
        chance = random.randint(1, 140)
    elif stats.level <= 24:
        chance = random.randint(1, 110)
    elif stats.level >= 25:
        chance= random.randint(1, 90)
    return chance


def update_power_ups(sound, sb, screen_rect, stats, ship, power_ups,
                     health_drops):
    '''
    if there is a power up is on screen make it move down by callling 
    its update function.
    '''
    # drop down
    if power_ups:
        for power_up in power_ups:
            power_up.update_power_up()

            # deleting missed power_ups.
            check_missed_power_up(screen_rect, power_up, power_ups)

            # check if any power ups have collided with the ship.
            collisions = ship_power_up_collisions(ship, power_ups)

            # add power if collisions happened.
            bestow_power(sound, sb, stats, power_up, collisions, power_ups)

    if health_drops:
        for drop in health_drops:
            drop.update_health_drop()

            check_missed_health_drop(screen_rect, drop, health_drops)

            collisions = health_drop_collisions(ship, health_drops)

            add_health(stats, sb, collisions)


def add_health(stats, sb, collisions):
    if collisions and stats.ships_left < 3:
        stats.ships_left += 1
        sb.prep_ships()


def check_missed_health_drop(screen_rect, drop, health_drops):
    if drop.rect.top >= screen_rect.bottom:
        drop.remove(health_drops)

def check_missed_power_up(screen_rect, power_up, power_ups):
    '''deleting missed power_ups.'''
    if power_up.rect.top >= screen_rect.bottom:
        power_ups.remove(power_up)


def bestow_power(sound, sb, stats, power_up, collisions, power_ups):
    '''add power if collision happend.'''
    if collisions:
        # add power_up to activates powers
        add_power_to_activated_powers(stats, collisions, power_ups)
        
        # give_power.
        power_up.give_power()
        
        # insert hint for the first time.
        if isinstance(power_up, MachineGunPowerUp) and not stats.hint_activated:
            sb.prep_hint()
            stats.hint_activated = True

        # activate sound
        sound.got_power_up()


def ship_power_up_collisions(ship, power_ups):
    '''determine collision between ship and powerup.'''
    collisions = pygame.sprite.spritecollide(ship, power_ups, True)
    return collisions


def health_drop_collisions(ship, health_drops):
    '''ship health drop collisisons.'''
    collisions = pygame.sprite.spritecollide(ship, health_drops, True)
    return collisions
    

def add_power_to_activated_powers(stats, collisions, power_ups):
    '''if power up is already active reset timer else add it to active powers.'''
    if collisions:
        for collision in collisions:    
            if not collision.permanent:
                '''not permenant'''
                # god_bullet.
                if isinstance(collision, GodBulletPowerUp):
                    if stats.god_bullet_active:
                        stats.reset_god_bullet_timer = True
                    else:
                        stats.active_powers.add(collision)

                # machine_gun.
                if isinstance(collision, MachineGunPowerUp):
                    if stats.machine_gun_active:
                        stats.reset_machine_gun_timer = True
                    else:
                        stats.active_powers.add(collision)
                    
            elif collision.permanent:
                '''permanent'''
                # mantis.
                if isinstance(collision, MantisPowerUp):
                    stats.permanent_powers.add(collision)
                    power_ups.remove(collision)

                # mantis God.
                elif isinstance(collision, MantisGodPowerUp):
                    for power in stats.permanent_powers:
                        power.end_power()
                    stats.permanent_powers.empty()
                    stats.permanent_powers.add(collision)
                    power_ups.remove(collision)
                
def end_power(ai_settings, stats, active_powers):
    '''
    End the power of each power up recpectively 
    once their time limit has been reached.
    '''
    if active_powers:
        # get_current time
        now = pygame.time.get_ticks()

        for power in active_powers:
            # if a already have a power_up reset its timer.
            reset_timers(stats, power)
            if isinstance(power, GodBulletPowerUp):
                if now - power.start_time >= ai_settings.god_bullet_timer:
                    power.end_power()
                    active_powers.remove(power)
            elif isinstance(power, MachineGunPowerUp):
                if now - power.start_time >= ai_settings.machine_gun_timer:
                    power.end_power()
                    active_powers.remove(power)


def reset_timers(stats, power):
    '''if already have a power up reset timer.'''
    # god_bullet.
    if isinstance(power, GodBulletPowerUp) and stats.reset_god_bullet_timer:
        power.get_start_time()
        stats.reset_god_bullet_timer = False
    # machine_gun.
    elif isinstance(power, MachineGunPowerUp) and stats.reset_machine_gun_timer:
        power.get_start_time()
        stats.reset_machine_gun_timer = False


def check_level(ai_settings, stats):
        '''check levels and turn on hard or insane mode.'''
        # if level is >= 6 turn on hard mode and dont increase speed.
        if stats.level >= 6 and stats.level < 12:
            stats.hard_mode = True
        # if its 12 or higher turn on insane mode.
        elif stats.level >= 14:
            stats.hard_mode = False
            stats.insane_mode = True
        ai_settings.increase_speed()


def add_score(ai_settings, stats, sb, collisions, sound):
    '''add score and check if high score is broken'''
    for aliens in collisions.values():
        stats.score += ai_settings.alien_points * len(aliens)
        sb.prep_score()
    check_high_score(stats, sb, sound)


def check_high_score(stats, sb, sound):
    '''Check to see if high score has been broken.'''
    compare(stats, sound)
    if stats.high_score_beat:
        sb.prep_high_score()


def create_fleet(ai_settings, screen, stats, ship, aliens):
    '''Create a full fleet of aliens.'''
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen, stats)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                   alien.rect.height)
    
    # Create first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, stats, aliens, alien_number,
                         row_number)


def get_number_aliens_x(ai_settings, alien_width):
    '''Determine the number of aliens that fit in a row.'''
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    '''Determine the number of rows of aliens that fit on the screen.'''
    available_space_y = (ai_settings.screen_height -
                         (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(ai_settings, screen, stats, aliens, alien_number, row_number):
    '''Create alien and add to the row.'''
    alien = Alien(ai_settings, screen, stats)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien) 


def close_game(stats, sound):
    '''save game before closing'''
    # Save high scores.
    save_game(stats, sound)

    # Close game.
    sys.exit()
    

def save_game(stats, sound):
    save_path = Path("saves/save_data.json")
    compare(stats, sound)
    high_scores = {
                  "high" : round(stats.high_score, -1),
                  "high_2" : round(stats.high_2, -1),
                  "high_3" : round(stats.high_3, -1),
                  }
    high_scores = json.dumps(high_scores)
    save_path.write_text(high_scores)


def compare(stats, sound):
    if stats.score > stats.high_score:
        if not stats.high_score_beat:
            stats.high_3 = stats.temp_2
            stats.high_2 = stats.high_score
            stats.high_score_beat = True

        stats.high_score = stats.score
        high_score_beat(stats, sound)

    elif stats.score > stats.high_2 and not stats.score == stats.high_score:
        if not stats.high_2_beat:
            stats.temp_2 = stats.high_2
            stats.high_3 = stats.high_2
            stats.high_2_beat = True
        stats.high_2 = stats.score

    elif stats.score > stats.high_3 and stats.score != stats.high_score and\
        stats.score != stats.high_2:
        stats.high_3 = stats.score

def high_score_beat(stats, sound):
    """everythin that happenes once high_score is broken"""

    # Play sound effect once.
    if not stats.run_high_score_s:
        sound.high_score_broke()
        # Finish loop.
        stats.run_high_score_s = True


def update_music(stats, sound):
    # Determine which music to play.
    if not stats.music_playing:
        if not stats.game_active: 
            sound.menu_music()
            stats.music_playing = True

        elif stats.game_active:
            sound.bg_music()
            stats.music_playing = True

