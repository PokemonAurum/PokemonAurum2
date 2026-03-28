.include "asm/include/battle_commands.inc"

.data

_000:
    // {0} is winded and cannot move!
    PrintMessage 1634, TAG_NICKNAME, BATTLER_CATEGORY_ATTACKER
    Wait
    WaitButtonABTime 30
    PlayBattleAnimation BATTLER_CATEGORY_ATTACKER, BATTLE_ANIMATION_WINDED
    Wait
    UnlockMoveChoice BATTLER_CATEGORY_ATTACKER
    End
    