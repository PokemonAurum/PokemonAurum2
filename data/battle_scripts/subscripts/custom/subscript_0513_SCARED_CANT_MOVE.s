.include "asm/include/battle_commands.inc"

.data

_000:
    // {0} was too scared to move!
    PrintMessage 1698, TAG_NICKNAME, BATTLER_CATEGORY_ATTACKER
    Wait
    WaitButtonABTime 30
    PlayBattleAnimation BATTLER_CATEGORY_ATTACKER, BATTLE_ANIMATION_SCARED
    Wait
    UnlockMoveChoice BATTLER_CATEGORY_ATTACKER
    End
