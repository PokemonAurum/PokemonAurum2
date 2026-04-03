.include "asm/include/battle_commands.inc"

.data

_000:
    CheckAbility CHECK_OPCODE_HAVE, BATTLER_CATEGORY_MSG_TEMP, ABILITY_MAGIC_GUARD, _end
    // {0} is hurt by the drenching!
    PrintMessage 1643, TAG_NICKNAME, BATTLER_CATEGORY_MSG_TEMP
    Wait
    WaitButtonABTime 30
    PlayBattleAnimation BATTLER_CATEGORY_MSG_TEMP, BATTLE_ANIMATION_DRENCHED
    Wait
    UpdateVar OPCODE_FLAG_ON, BSCRIPT_VAR_BATTLE_STATUS, BATTLE_STATUS_NO_BLINK
    GoToSubscript BATTLE_SUBSCRIPT_UPDATE_HP
    Call BATTLE_SUBSCRIPT_SWITCH_IN_ABILITY_CHECK

_end:
    End
    