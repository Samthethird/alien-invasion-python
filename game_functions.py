from bullet import Bullet
from alien import Alien
from time import sleep
from ship import Ship
import pygame
import sys

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
                 bullets, sound):
    '''Respond to keyboard an mouse activity.'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            close_game(ai_settings, stats)
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship,
                                 aliens, bullets, sound)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens,
                              bullets, mouse_x, mouse_y)
            

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, 
                      bullets, mouse_x, mouse_y):
    '''Start a game when the player hits the play button.'''
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked:
        start_game(ai_settings, screen, stats, sb, ship, aliens, bullets)
        stats.game_counter += 1


def check_keyup_events(event, ship):
    '''Respond to key releases.'''
    if event.key == pygame.K_d:
        ship.moving_right = False
    elif event.key == pygame.K_a:
        ship.moving_left = False


def check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets, sound):
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
        start_game(ai_settings, screen, stats, ship, aliens, bullets)


def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets):
    if not stats.game_active:
        # Reset the games settings.
        ai_settings.initialize_dynamic_settings()

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


def close_game(ai_settings, stats):
    '''save game before closing'''
    # Save high score.
    with open(ai_settings.data_location, 'w') as high_score:
        high_score.write(str(stats.high_score))
    
    # Close game.
    sys.exit()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
                  play_button, sound):
    '''Update the images on screen and flip to a new screen.'''
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)

    if stats.game_active:
        # Redraw all the bullets behind ship and alliens.
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        
        ship.blitme()
        aliens.draw(screen)

    # Draw the play button and the menu if the game is inactive.
    elif not stats.game_active:
        play_button.draw_button()

        # Draw the main menu.
        create_menu(ai_settings, screen)
        high_score_beat_menu(stats, sb, sound)
        
    # Draw score information.
    sb.show_score()

    # Display the most recent screen.
    pygame.display.flip()


def create_menu(ai_settings, screen):
    '''Make the main menu art.'''
    create_menu_alien(ai_settings, screen)
    create_menu_bullet(ai_settings, screen)
    create_menu_ship(ai_settings, screen)


def create_menu_alien(ai_settings, screen):
    '''Create an alien for the main menu art.'''
    solo_alien = Alien(ai_settings, screen)
    solo_alien.rect.x = 200
    solo_alien.rect.y = 250
    solo_alien.blitme()


def create_menu_ship(ai_settings, screen):
    '''Create a ship for the amin menu art.'''
    solo_ship = Ship(ai_settings, screen)
    solo_ship.rect.x = 200
    solo_ship.rect.y = 470
    solo_ship.blitme()


def create_menu_bullet(ai_settings, screen):
    '''Create a bullet for the main menu art.'''
    rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                       ai_settings.bullet_height)
    rect.x = 230
    rect.y = 400
    pygame.draw.rect(screen, ai_settings.bullet_color, rect)


def high_score_beat_menu(stats, sb, sound):
    '''if highscore beat display achivement and sound-effect.'''
    if not stats.game_active:
        sb.prep_achivement()
        sb.draw_achivement()

    if not stats.game_active and stats.game_over_s and stats.high_score_beat:
        # Initiate winning audio.
        sound.high_score_beat()

        # ending loop
        stats.game_over_s = False

    elif not stats.game_active and stats.game_over_s:
        # Initiate losing audio.
        sound.high_score_not_beat()

        # ending loop
        stats.game_over_s = False


def fire_bullet(ai_settings, screen, ship, bullets, sound):
    '''Make a bullet if limit not reached.'''
    # Create a bullet and add it to the bullets group.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

        #initiate sound effect.
        sound.fire_bullet()

def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    '''
    Check if any alien has reached an edge then change
    fleet direction, and check for bottomm and ship collissions.
    '''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Detecting ship-alien collisison.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
    
    # Look for aliens hitting the bottom of the screen.
    check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)


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

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
    '''Check for any aliens that reached the bottom of the screen.'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            '''Respond as if the ship is hit.'''
            ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
            break


def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
    '''Respond properly if the ship is hit.'''
    if stats.ships_left > 1:
        next_life(ai_settings, stats, sb, screen, ship, aliens, bullets)
    else:
        alien_hit_s = pygame.mixer.Sound("sound_effects/ship_hit.wav")
        alien_hit_s.set_volume(0.2)
        alien_hit_s.play()

        # pause
        sleep(0.5)
        stats.game_active = False
        stats.game_over_s = True
        pygame.mouse.set_visible(True)


def update_bullet(ai_settings, screen, stats, sb, ship, aliens, bullets, sound):
    '''Update position of bullets and remove old ones.'''
    # Update bullet positions
    bullets.update()
    
    # Deleting unececary bullets.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, bullets, aliens, sound)


def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, bullets, aliens, sound):
    '''Respond to bullet/alien collisions.'''

    # Remove any bullet and alines that have collided
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        '''If  entire fleet is destroyed, go to new level'''
        next_level(ai_settings, screen, stats, sb, ship, bullets, aliens)
    
    # increase score if alien hit.
    add_score(ai_settings, stats, sb, collisions, sound)


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

        # Play sound effect once.
        if stats.run_high_score_s:

            # Initiate sound effect.
            sound.high_score_broke()

            # beat high score.
            stats.high_score_beat = True

            # Finish loop.
            stats.run_high_score_s = False


def next_level(ai_settings, screen, stats, sb, ship, bullets, aliens):
        '''proceed to the next level.'''
        # initate sound effect
        new_level_s = pygame.mixer.Sound("sound_effects/next_level.wav")
        new_level_s.set_volume(0.2)
        new_level_s.play()

        bullets.empty()
        ai_settings.increase_speed()

        create_fleet(ai_settings, screen, ship, aliens)

        # Increase level.
        stats.level += 1
        sb.prep_level()


def next_life(ai_settings, stats, sb, screen, ship, aliens, bullets):
    '''go to next ship and reset level'''
    alien_hit_s = pygame.mixer.Sound("sound_effects/ship_hit.wav")
    alien_hit_s.set_volume(0.2)
    alien_hit_s.play()

    # Decrement ships left.
    stats.ships_left -= 1

    # Update scoreboard ships
    sb.prep_ships()

    # Empty the groups of aliens and bullets.
    aliens.empty()
    bullets.empty()

    # Create new feet and and center ship.
    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()

    # Pause.
    sleep(0.5)


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