import pygame

pygame.mixer.init()

"""load music """

pygame.mixer.music.load("assets/audio/J. Cole - Huntin' Wabbitz.mp3")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1,0.0,5000)

shot_fx = pygame.mixer.Sound("assets/audio/arrow_shot.mp3")
shot_fx.set_volume(0.5)
hit_fx = pygame.mixer.Sound("assets/audio/arrow_hit.wav")
monster_death_fx = pygame.mixer.Sound("assets/audio/squeek.wav")
player_m_hit_fx = pygame.mixer.Sound("assets/audio/player_m_hit.mp3")
player_m_death_fx = pygame.mixer.Sound("assets/audio/death_sound.wav")
player_f_hit_fx = pygame.mixer.Sound("assets/audio/player_f_hit.mp3")
player_f_death_fx = pygame.mixer.Sound("assets/audio/player_f_death.opus")
walk_1_fx =  pygame.mixer.Sound("assets/audio/walk_1.mp3")
walk_2_fx =  pygame.mixer.Sound("assets/audio/walk_2.mp3")
demon_death_fx = pygame.mixer.Sound("assets/audio/demon_death.mp3")
ogre_death_fx = pygame.mixer.Sound("assets/audio/ogre_death.mp3")
ogre_roar_fx = pygame.mixer.Sound("assets/audio/ogre_roar.mp3")
zombie_growl_fx = pygame.mixer.Sound("assets/audio/zombie_growl.mp3")
coin_fx = pygame.mixer.Sound("assets/audio/coin.wav")
potion_fx = pygame.mixer.Sound("assets/audio/heal.wav")
lightning_fx = pygame.mixer.Sound("assets/audio/lightning.wav")
fire_fx = pygame.mixer.Sound("assets/audio/fire.wav")
intro_fx = pygame.mixer.Sound("assets/audio/intro_heavy.opus")
fireball_fx = pygame.mixer.Sound("assets/audio/fireball_fx.mp3")
wizard_hit_fx = pygame.mixer.Sound("assets/audio/wizard_hit_fx.opus")
wizard_death_fx = pygame.mixer.Sound("assets/audio/wizard_death_fx.opus")

sound_effects = {"shot_fx":shot_fx,"hit_fx":hit_fx,"player_m_death_fx":player_m_death_fx,
                 "player_m_death_fx":player_m_death_fx,
                 "monster_death_fx":monster_death_fx
                 ,"demon_death_fx":demon_death_fx,"ogre_death_fx":ogre_death_fx,"ogre_roar_fx":ogre_roar_fx,
                 "zombie_growl_fx":zombie_growl_fx,"coin_fx":coin_fx,"potion_fx":potion_fx,
                 "lightning_fx":lightning_fx,"fire_fx":fire_fx,"player_m_hit_fx":player_m_hit_fx,
                 "player_f_hit_fx":player_f_hit_fx,"player_f_death_fx":player_f_death_fx,"walk_1_fx":walk_1_fx,"walk_2_fx":walk_2_fx,
                 "fireball_fx":fireball_fx,"wizard_death_fx":wizard_death_fx,"wizard_hit_fx":wizard_hit_fx,"fireball_fx":fireball_fx}
