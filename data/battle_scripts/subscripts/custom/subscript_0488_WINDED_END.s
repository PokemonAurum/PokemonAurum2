.include "asm/include/battle_commands.inc"

.data

_000:
    // {0} shook off the wind!
    PrintMessage 1637, TAG_NICKNAME, BATTLER_CATEGORY_MSG_TEMP
    Wait
    SetHealthbarStatus BATTLER_CATEGORY_MSG_TEMP, BATTLE_ANIMATION_NONE
    WaitButtonABTime 30
    End
    