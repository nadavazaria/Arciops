import pygame

pygame.mixer.init()

"""load music """
music = pygame.mixer.music 
music.load("assets/audio/J. Cole - Huntin' Wabbitz.mp3")
# music.play(-1,0.0,5000)

shot_fx = pygame.mixer.Sound("assets/audio/arrow_shot.mp3")
player_m_hit_fx = pygame.mixer.Sound("assets/audio/player_m_hit.mp3")
player_m_death_fx = pygame.mixer.Sound("assets/audio/death_sound.wav")
player_f_hit_fx = pygame.mixer.Sound("assets/audio/player_f_hit.mp3")
player_f_death_fx = pygame.mixer.Sound("assets/audio/player_f_death.opus")
walk_1_fx =  pygame.mixer.Sound("assets/audio/walk_1.mp3")
walk_2_fx =  pygame.mixer.Sound("assets/audio/walk_2.mp3")
lightning_fx = pygame.mixer.Sound("assets/audio/lightning.wav")
fireball_fx = pygame.mixer.Sound("assets/audio/fireball_fx.mp3")
wizard_hit_fx = pygame.mixer.Sound("assets/audio/wizard_hit_fx.opus")
wizard_death_fx = pygame.mixer.Sound("assets/audio/wizard_death_fx.opus")
fire_fx = pygame.mixer.Sound("assets/audio/fire.wav")
player_sfx = [fire_fx,lightning_fx,player_f_death_fx,walk_1_fx,walk_2_fx,shot_fx,
              player_m_hit_fx,player_m_death_fx,player_f_hit_fx,wizard_death_fx,wizard_hit_fx,fireball_fx]

hit_fx = pygame.mixer.Sound("assets/audio/arrow_hit.wav")
demon_death_fx = pygame.mixer.Sound("assets/audio/demon_death.mp3")
ogre_death_fx = pygame.mixer.Sound("assets/audio/ogre_death.mp3")
ogre_roar_fx = pygame.mixer.Sound("assets/audio/ogre_roar.mp3")
zombie_growl_fx = pygame.mixer.Sound("assets/audio/zombie_growl.mp3")
summon_fx =  pygame.mixer.Sound("assets/audio/summon_fx.mp3")
magical_spell_fx =  pygame.mixer.Sound("assets/audio/magical_spell_fx.mp3")
spawn_fx = pygame.mixer.Sound("assets/audio/monster_death.wav")
spawn_fx.set_volume(0.2)
monster_death_fx = pygame.mixer.Sound("assets/audio/squeek.wav")
monster_stx = [hit_fx,demon_death_fx,ogre_death_fx,ogre_roar_fx,zombie_growl_fx,spawn_fx,monster_death_fx,summon_fx,spawn_fx,magical_spell_fx]

coin_fx = pygame.mixer.Sound("assets/audio/coin.wav")
potion_fx = pygame.mixer.Sound("assets/audio/heal.wav")
buy_item_fx = pygame.mixer.Sound("assets/audio/buy_item.mp3")
game_sound = [coin_fx,buy_item_fx,potion_fx,walk_1_fx,walk_2_fx]

sound_effects = {"shot_fx":shot_fx,"hit_fx":hit_fx,"player_m_death_fx":player_m_death_fx,
                 "player_m_death_fx":player_m_death_fx,
                 "monster_death_fx":monster_death_fx
                 ,"demon_death_fx":demon_death_fx,"ogre_death_fx":ogre_death_fx,"ogre_roar_fx":ogre_roar_fx,
                 "zombie_growl_fx":zombie_growl_fx,"coin_fx":coin_fx,"potion_fx":potion_fx,
                 "lightning_fx":lightning_fx,"fire_fx":fire_fx,"player_m_hit_fx":player_m_hit_fx,
                 "player_f_hit_fx":player_f_hit_fx,"player_f_death_fx":player_f_death_fx,"walk_1_fx":walk_1_fx,"walk_2_fx":walk_2_fx,
                 "fireball_fx":fireball_fx,"wizard_death_fx":wizard_death_fx,"wizard_hit_fx":wizard_hit_fx,"fireball_fx":fireball_fx,
                 "spawn_fx":spawn_fx,"summon_fx":summon_fx,"magical_spell_fx":magical_spell_fx}
