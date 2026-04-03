.include "asm/include/battle_commands.inc"

.data

_000:
    // {0} was too winded to follow through!
    PrintMessage 1694, TAG_NICKNAME, BATTLER_CATEGORY_ATTACKER
    Wait
    WaitButtonABTime 30
    End
