// Test: Full Heal item clears condition3 (custom volatile status) on the target battler
//
// Validates that using a Full Heal (or Full Restore) during battle correctly clears
// condition3 flags and associated turn counters via ClearCondition3 (opcode 0x116),
// which was wired into subscript_0268_USE_STATUS_RECOVERY and
// subscript_0289_USE_FULL_RESTORE.
//
// FRAMEWORK LIMITATIONS — two additions are needed before this test can run:
//
//   1. ACTION_USE_ITEM is not implemented.
//      The action table (test_battle.h) only supports move slots (0-3) and switch
//      slots (4-9). Item use during battle requires a new action code plus a way to
//      specify the item ID and target battler, e.g.:
//        #define ACTION_USE_ITEM  10
//      and a corresponding field in BattleAction (currently only u8 action + u8 target).
//
//   2. EXPECTATION_TYPE_CONDITION3 is not implemented.
//      The expectation system (ExpectationType enum, test_battle.h) has no way to
//      assert on battlemon[x].condition3 after the scenario runs. A new type is needed,
//      e.g. EXPECTATION_TYPE_CONDITION3_CLEAR, that reads sp->battlemon[slot].condition3
//      and verifies it equals 0.
//
// Until both are added, this test is marked knownFailing = 1 so it is tracked but
// does not block CI.

#ifndef GET_TEST_CASE_ONLY

#include "../../../../include/battle.h"
#include "../../../../include/constants/ability.h"
#include "../../../../include/constants/item.h"
#include "../../../../include/constants/moves.h"
#include "../../../../include/constants/species.h"
#include "../../../../include/test_battle.h"
#include "../../../../include/constants/battle_message_constants.h"

const struct TestBattleScenario BattleTests[] = {

#endif

    {
        .battleType    = BATTLE_TYPE_SINGLE,
        .weather       = WEATHER_NONE,
        .fieldCondition = 0,
        .terrain       = TERRAIN_NONE,

        .playerParty = {
            {
                .species   = SPECIES_WOOPER,
                .level     = 50,
                .form      = 0,
                .ability   = ABILITY_WATER_ABSORB,
                .item      = ITEM_FULL_HEAL,    // item the trainer will use
                .moves     = { MOVE_TACKLE, MOVE_NONE, MOVE_NONE, MOVE_NONE },
                .hp        = FULL_HP,
                .status    = 0,
                .condition2 = 0,
                // Pre-seed condition3 so the test starts with the status active.
                .condition3 = CONDITION3_DRENCHED,
                .winded_turns    = 0,
                .awestruck_turns = 0,
                .migraine_turns  = 0,
                .idolize_turns   = 0,
                .moveEffectFlags = 0,
            },
            { .species = SPECIES_NONE },
            { .species = SPECIES_NONE },
            { .species = SPECIES_NONE },
            { .species = SPECIES_NONE },
            { .species = SPECIES_NONE },
        },

        .enemyParty = {
            {
                .species   = SPECIES_WOOPER,
                .level     = 50,
                .form      = 0,
                .ability   = ABILITY_WATER_ABSORB,
                .item      = ITEM_NONE,
                .moves     = { MOVE_TACKLE, MOVE_NONE, MOVE_NONE, MOVE_NONE },
                .hp        = FULL_HP,
                .status    = 0,
                .condition2 = 0,
                .condition3 = 0,
                .winded_turns    = 0,
                .awestruck_turns = 0,
                .migraine_turns  = 0,
                .idolize_turns   = 0,
                .moveEffectFlags = 0,
            },
            { .species = SPECIES_NONE },
            { .species = SPECIES_NONE },
            { .species = SPECIES_NONE },
            { .species = SPECIES_NONE },
            { .species = SPECIES_NONE },
        },

        // TODO: Replace ACTION_MOVE_SLOT_1 with ACTION_USE_ITEM targeting
        // BATTLER_PLAYER_FIRST once item-use actions are supported.
        // For now, the player just attacks so the scenario can compile and run.
        .playerScript = {
            {
                { ACTION_MOVE_SLOT_1, BATTLER_ENEMY_FIRST }, // placeholder — should be USE_ITEM
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
            },
            {
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
            },
        },

        .enemyScript = {
            {
                { ACTION_MOVE_SLOT_1, BATTLER_PLAYER_FIRST },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
            },
            {
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
                { ACTION_NONE, 0 },
            },
        },

        // TODO: Replace with EXPECTATION_TYPE_CONDITION3_CLEAR once that expectation
        // type is added to the framework. The expectation should assert:
        //   battlemon[BATTLER_PLAYER_FIRST].condition3 == 0
        // For now, no expectations are set so the test trivially passes structurally
        // but does not actually validate the behaviour.
        .expectations = { { 0 } },

        .expectationPassCount = 0,
        .knownFailing = 1,  // remove once ACTION_USE_ITEM + EXPECTATION_TYPE_CONDITION3 exist
    },

#ifndef GET_TEST_CASE_ONLY
};
#endif
