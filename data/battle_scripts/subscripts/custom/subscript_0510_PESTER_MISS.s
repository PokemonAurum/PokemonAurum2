.include "asm/include/battle_commands.inc"

.data

_000:
    // {0} was too itchy to aim!
    PrintMessage 1693, TAG_NICKNAME, BATTLER_CATEGORY_ATTACKER
    Wait
    WaitButtonABTime 30
    End
