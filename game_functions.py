from power_up_god_bullet import GodBulletPowerUp
from bullet import Bullet
from alien import Alien
from time import sleep
import pygame
import random
import sys


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets, sound):
    '''Respond to keyboard an mouse activity.'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_game(ai_settings, stats)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, sb, ship,
                                 aliens, bullets, sound)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
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


def check_keyup_events(event, ship):
    '''Respond to key releases.'''
    if event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_a:
        ship.moving_left = False


def check_keydown_events(event, ai_settings, screen, stats, sb, ship, aliens, bullets, sound):
    '''Respond to key presses.'''
    if event.key == pygame.K_d:
        ship.moving_right = True
    elif event.key == pygame.K_a:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets, sound)
    elif event.key == pygame.K_q:
        close_game(ai_settings, stats)
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets, sound)
    elif event.key == pygame.K_f:
        stats.ships_left = 0
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, sound)


def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets, sound):
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

        # Create new fleet and center ship.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button, sound, menu_art, power_ups):
    '''Update the images on screen and flip to a new screen.'''
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)

    if stats.game_active:
        # Redraw all the bullets behind ship and alliens.
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        
        ship.blitme()
        aliens.draw(screen)
        
        # draw each power_up currently on screen.
        if power_ups:
            for power_up in power_ups.sprites():
                power_up.draw_power_up()


    # Draw the play button and the menu if the game is inactive.
    elif not stats.game_active:
        play_button.draw_button()

        # Draw the main menu.
        menu_art.create_menu_art()
        display_menu_achivement(stats, sb, sound)
        
    # Draw score information.
    sb.show_score()

    # Display the most recent screen.
    pygame.display.flip()


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


def fire_bullet(ai_settings, screen, ship, bullets, sound):
    '''Make a bullet if limit not reached.'''
    # Create a bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

        #initiate sound effect.
        sound.fire_bullet()


def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets, sound):
    '''
    Check if any alien has reached an edge then change
    fleet direction, and check for bottom and ship collisions.
    '''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Detecting ship-alien collisions.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, sound)
    
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets, sound)


def check_fleet_edges(ai_settings, aliens):
    '''Respond appropriately if any aliens have reached an edge.'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    '''Drop the entire fleet and change directions.'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets, sound):
    '''Check for any aliens that reached the bottom of the screen.'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            '''Respond as if the ship is hit.'''
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, sound)
            break


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets, sound):
    '''Respond properly if the ship is hit.'''
    if stats.ships_left > 1:
        next_life(ai_settings, stats, sb, screen, ship, aliens, bullets, sound)
    else:
        # Initiate hit audio.
        sound.ship_hit()

        # pause, finish game, activate gameover sound and make cursor visable.
        sleep(0.5)
        stats.game_active = False
        stats.game_over_s = True
        
        # Reset music played.
        stats.reset_music()
        pygame.mouse.set_visible(True)


def next_life(ai_settings, stats, sb, screen, ship, aliens, bullets, sound):
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

    # Create new fleet and and center ship.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # Pause.
    sleep(0.5)


def update_bullet(ai_settings, screen, stats, sb, ship, aliens, bullets, sound, power_ups):
    '''Update position of bullets and remove old ones and check for alien bullet collisisons.'''
    # Update bullet positions
    bullets.update()
    
    # Deleting unececary bullets.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, bullets, aliens, sound, power_ups)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, bullets, aliens, sound, power_ups):
    '''Respond to bullet/alien collisions.'''

    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, ai_settings.bullet_destruction, True)

    # randomly drop a powerup if an alien is killed.
    drop_power_up(ai_settings, screen, power_ups, collisions)

    if len(aliens) == 0:
        '''If  entire fleet is destroyed, go to new level'''
        next_level(ai_settings, screen, stats, sb, ship, bullets, aliens, sound)
    
    # increase score if alien hit.
    add_score(ai_settings, stats, sb, collisions, sound)


def drop_power_up(ai_settings, screen, power_ups, collisions):
    '''Randomly drop a powerup when and alien is killed.'''
    if collisions:
        #roll a dice to determine power_up drop
        chance = 1

        if chance == 1:
            # if dice rolled 1 drop a "GodBullet" powerup.
            for aliens in collisions.values():
                for alien in aliens:
                    god_bullet_power_up = GodBulletPowerUp(ai_settings, screen, alien)
                    power_ups.add(god_bullet_power_up)


def update_power_ups(screen_rect, stats, ship, power_ups, active_powers):
    '''
    if there is a power up is on screen make it move down by callling 
    its update function.
    '''
    # drop down
    if power_ups:
        for power_up in power_ups:
            power_up.update_power_up()

            # deleting missed power_ups.
            if power_up.rect.top >= screen_rect.bottom:
                power_ups.remove(power_up)

            # check if any power ups have collided with the ship.
            collisions = ship_power_up_collisions(stats, ship, power_ups)
            if collisions:
                # give respective power if collisions happend.
                power_up.give_power()
            

def ship_power_up_collisions(stats, ship, power_ups):
    '''determine collision between ship and powerup.'''
    collisions = pygame.sprite.spritecollide(ship, power_ups, True)
    activate_powers(stats, collisions)
    return collisions


def activate_powers(stats, collisions):
    stats.active_powers.add(collisions)


def end_power(ai_settings, active_powers):
    '''
    End the power of each power up recpectively 
    once their time limit has been reached.
    '''
    if active_powers:
        now = pygame.time.get_ticks()
        for power in active_powers:
            if now - power.start_time >= ai_settings.god_bullet_timer:
                ai_settings.reset_god_bullet_settings()
                active_powers.remove(power)


def next_level(ai_settings, screen, stats, sb, ship, bullets, aliens, sound):
        '''proceed to the next level.'''
        # initate next level sound effect.
        sound.next_level()

        # Empty bullets and increase game speed
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

        # Increase and show level.
        stats.level += 1
        sb.prep_level()


def add_score(ai_settings, stats, sb, collisions, sound):
    if collisions:
        '''add score and check if high score is broken'''
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb, sound)


def check_high_score(stats, sb, sound):
    '''Check to see if high score has been broken.'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
        stats.high_score_beat = True

        # Play sound effect once.
        if not stats.run_high_score_s:
            sound.high_score_broke()

            # Finish loop.
            stats.run_high_score_s = True


def create_fleet(ai_settings, screen, ship,  aliens):
    '''Create a full fleet of aliens.'''
    # Create an alien and find the number of aliens in a row.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                   alien.rect.height)
    
    # Create first row of aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
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


def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    '''Create alien and add to the row.'''
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien) 


def close_game(ai_settings, stats):
    '''save game before closing'''
    # Save high score.
    with open(ai_settings.data_location, 'w') as high_score:
        high_score.write(str(stats.high_score))
    
    # Close game.
    sys.exit()


def update_music(stats, sound):
    # Determine which music to play.
    if not stats.music_playing:
        if not stats.game_active: 
            sound.menu_music()
            stats.music_playing = True

        elif stats.game_active:
            sound.bg_music()
            stats.music_playing = True

