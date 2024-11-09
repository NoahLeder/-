import sys
from time import sleep
from gc import collect

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship

from bullet import Bullet

from alien import Alien
from button import Button

from scoreboard import Scoreboard

class Game:#管理游戏的资源和行为类
    def __init__(self):
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        #全屏
        #self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("game")
        #创建一个用于存储数据信息的实例
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)

        self.bullets = pygame.sprite.Group()

        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        #设置背景色
        self.bg_color = pygame.Color(self.settings.bg_color)

        #启动游戏后处于活动状态
        self.game_active = False

        #创建play按钮
        self.play_button = Button(self,"lets go")
    def _ship_hit(self):
        """响应飞船和外星人的碰撞"""
        if self.stats.ships_left >0:
            #将ship_left减1
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            #清空外星人列表和子弹
            self.bullets.empty()
            self.aliens.empty()

            #创建一个新的外形舰队
            self._create_fleet()
            self.ship.center_ship()

            #暂停
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
    def _create_fleet(self):
        """创建一个外形舰队"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3*alien_height):
            while current_x < (self.settings.screen_width - 2*alien_width):
                self._create_alien(current_x,current_y)
                current_x += 2*alien_width
            current_x = alien_width
            current_y += 2*alien_height

    def _create_alien(self,x_position,y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def run_game(self):#开始游戏的主循环
        while True:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
            self.clock.tick(60)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        #检查是否有外星人到达屏幕的下边缘
        self._check_aliens_bottom()

    def _update_bullets(self):
        self.bullets.update()
        # 删除已经消失的子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        print(len(self.bullets))
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score +=self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            #提高等级
            self.stats.level += 1
            self.sb.prep_level()

    def _check_events(self):
                #侦听键盘和鼠标事件
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        self._check_keydown_events(event)
                    elif event.type == pygame.KEYUP:
                        self._check_keyup_events(event)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = pygame.mouse.get_pos()
                        self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家单击按钮开始游戏"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
        #if self.play_button.rect.collidepoint(mouse_pos):
            #还原游戏设置
            self.settings.initialize_dynamic_settings()
            #隐藏光标
            pygame.mouse.set_visible(False)
            #充值游戏的统计信息
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            #清空外星人列表和子弹列表
            self.bullets.empty()
            self.aliens.empty()
            #创建一个新的外形舰队，并将飞船放在屏幕底部的中央
            self._create_fleet()
            self.ship.center_ship()
    def _check_keydown_events(self,event):
        if event.key == pygame.K_RIGHT:
            # 向右移动
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """创建一个子弹加入编组bullets"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


    def _update_screen(self):
                #每次循环都会重新绘制屏幕
                self.screen.fill(self.bg_color)
                for bullet in self.bullets.sprites():
                    bullet.draw_bullet()
                self.ship.blitme()
                self.aliens.draw(self.screen)
                #显示得分
                self.sb.show_score()
                #如果游戏处于非活动状态就绘制play
                if not self.game_active:
                    self.play_button.draw_button()

                #让最近绘制的屏幕可见
                pygame.display.flip()
    def _check_fleet_edges(self):
        """再有外星人到达边缘时采取相应的措施"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
    def _change_fleet_direction(self):
        """整个舰队向下移动并改变方向"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        #检测是否有外星人到达屏幕的下边缘
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                #像飞船被撞到一样处理
                self._ship_hit()
                break
if __name__ == '__main__':
    #创建游戏实例并运行游戏
    ai =Game()
    ai.run_game()

