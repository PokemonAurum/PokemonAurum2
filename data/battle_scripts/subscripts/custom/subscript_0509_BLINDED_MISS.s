.include "asm/include/battle_commands.inc"

.data

_000:
    // {0} could not see its target!
    PrintMessage 1692, TAG_NICKNAME, BATTLER_CATEGORY_ATTACKER
    Wait
    WaitButtonABTime 30
    End
