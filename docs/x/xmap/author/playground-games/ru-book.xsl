<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
    <xsl:include href="ru-include.xsl" />
    <xsl:template match="/book">
        <html lang="ru">
            <head>
                <title>
                    <xsl:value-of select="$title_ru" />
                </title>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <meta content="text/html; charset=utf-8" http-equiv="Content-type"/>
                <meta name="robots" content="INDEX,FOLLOW"/>
                <link rel="shortcut icon" href="favicon.ico" type="image/x-icon"/>
                <link rel="stylesheet" href="xbook.xgame/resources/default.css"/>
                <link rel="stylesheet" href="xbook.xgame/resources/style.css"/>
                <xsl:if test="$book_type='pdf'">
                    <script src="xbook.xgame/resources/paged.polyfill.js"/>
                </xsl:if>
            </head>
            <body>
                <div id="book">
                    <div id="section-00">
                        <xsl:copy-of select="$s00_begin__01_cover_ru" />
                        <xsl:copy-of select="$s00_begin__02_cover2_ru" />
                        <xsl:copy-of select="$s00_begin__03_annotation_ru" />
                        <xsl:copy-of select="$s00_begin__04_table_ru" />
                        <xsl:copy-of select="$s00_begin__05_intro_ru" />
                    </div>
                    <div id="section-01" class="page-break">
                        <a name="part_02" />
                        <h1>
                            <a href="#_part_02">
                                <xsl:value-of select="$s01_classic_games_ru" />
                            </a>
                        </h1>
                        <xsl:copy-of select="$s01_classic_games__01_chess_ru" />
                        <xsl:copy-of select="$s01_classic_games__02_checkers_ru" />
                    </div>
                    <div id="section-02" class="page-break">
                        <a name="part_03" />
                        <h1>
                            <a href="#_part_03">
                                <xsl:value-of select="$s02_with_dice_ru" />
                            </a>
                        </h1>
                        <xsl:copy-of select="$s02_with_dice__01_dice_chess_ru" />
                        <xsl:copy-of select="$s02_with_dice__02_random_chess_ru" />
                        <xsl:copy-of select="$s02_with_dice__03_chess_with_d12_ru" />
                        <xsl:copy-of select="$s02_with_dice__04_chess_with_3xd12_ru" />
                        <xsl:copy-of select="$s02_with_dice__05_random_other_ru" />
                    </div>
                    <div id="section-03" class="page-break">
                        <a name="part_04" />
                        <h1>
                            <a href="#_part_04">
                                <xsl:value-of select="$s03_other_start_ru" />
                            </a>
                        </h1>
                        <xsl:copy-of select="$s03_other_start__01_chess_960_ru" />
                        <xsl:copy-of select="$s03_other_start__02_DFRC_ru" />
                        <xsl:copy-of select="$s03_other_start__03_racing_kings_ru" />
                        <xsl:copy-of select="$s03_other_start__04_bad_chess_ru" />
                    </div>
                    <div id="section-04" class="page-break">
                        <a name="part_05" />
                        <h1>
                            <a href="#_part_05">
                                <xsl:value-of select="$s04_two_sets_ru" />
                            </a>
                        </h1>
                        <xsl:copy-of select="$s04_two_sets__01_bughouse_ru" />
                        <xsl:copy-of select="$s04_two_sets__02_alice_ru" />
                        <xsl:copy-of select="$s04_two_sets__03_horde_ru" />
                    </div>
                    <div id="section-05" class="page-break">
                        <a name="part_06" />
                        <h1>
                            <a href="#_part_06">
                                <xsl:value-of select="$s05_mini_sizes_ru" />
                            </a>
                        </h1>
                        <xsl:copy-of select="$s05_mini_sizes__01_3x3_chess_ru" />
                        <xsl:copy-of select="$s05_mini_sizes__02_3x4_chess_ru" />
                        <xsl:copy-of select="$s05_mini_sizes__03_4x4_chess_ru" />
                        <xsl:copy-of select="$s05_mini_sizes__04_5x5_gardner_mini_ru" />
                        <xsl:copy-of select="$s05_mini_sizes__05_6x6_los_alamos_ru" />
                    </div>
                    <div id="section-06" class="page-break">
                        <a name="part_07" />
                        <h1>
                            <a href="#_part_07">
                                <xsl:value-of select="$s06_add_figures_ru" />
                            </a>
                        </h1>
                        <xsl:copy-of select="$s06_add_figures__01_maharajah_ru" />
                        <xsl:copy-of select="$s06_add_figures__02_gothic_chess_ru" />
                        <xsl:copy-of select="$s06_add_figures__03_kapablanka_ru" />
                        <xsl:copy-of select="$s06_add_figures__04_grand_chess_ru" />
                        <xsl:copy-of select="$s06_add_figures__05_bear_chess_ru" />
                        <xsl:copy-of select="$s06_add_figures__06_berolina_ru" />
                        <xsl:copy-of select="$s06_add_figures__07_duck_ru" />
                        <xsl:copy-of select="$s06_add_figures__08_astral_ru" />
                    </div>
                    <div id="section-07" class="page-break">
                        <a name="part_08" />
                        <h1>
                            <a href="#_part_08">
                                <xsl:value-of select="$s07_with_pocket_ru" />
                            </a>
                        </h1>
                        <xsl:copy-of select="$s07_with_pocket__01_crazy_house_ru" />
                        <xsl:copy-of select="$s07_with_pocket__02_king_chess_ru" />
                    </div>
                    <div id="section-08" class="page-break">
                        <a name="part_09" />
                        <h1>
                            <a href="#_part_09">
                                <xsl:value-of select="$s08_other_rules_ru" />
                            </a>
                        </h1>
                        <xsl:copy-of select="$s08_other_rules__01_anti_chess_ru" />
                        <xsl:copy-of select="$s08_other_rules__02_anti_checkers_ru" />
                        <xsl:copy-of select="$s08_other_rules__03_three_check_ru" />
                        <xsl:copy-of select="$s08_other_rules__04_metamorph_ru" />
                        <xsl:copy-of select="$s08_other_rules__05_king_hill_ru" />
                        <xsl:copy-of select="$s08_other_rules__06_atomic_ru" />
                        <xsl:copy-of select="$s08_other_rules__07_marseillais_chess_ru" />
                        <xsl:copy-of select="$s08_other_rules__08_andernach_chess_ru" />
                        <xsl:copy-of select="$s08_other_rules__09_progressive_chess_ru" />
                    </div>
                    <div id="section-09" class="page-break">
                        <a name="part_10" />
                        <h1>
                            <a href="#_part_10">
                                <xsl:value-of select="$s09_other_games_ru" />
                            </a>
                        </h1>
                        <xsl:copy-of select="$s09_other_games__01_pawn_duel_ru" />
                        <xsl:copy-of select="$s09_other_games__02_rook_game_ru" />
                        <xsl:copy-of select="$s09_other_games__03_makruk_ru" />
                        <xsl:copy-of select="$s09_other_games__04_metamorph_dice_ru" />
                    </div>

                    <div id="section-99" class="page-break">
                        <xsl:copy-of select="$s99_end__01_ending_ru" />
                        <xsl:copy-of select="$s99_end__02_advert_ru" />
                        <xsl:copy-of select="$s99_end__98_backcover2_ru" />
                        <xsl:copy-of select="$s99_end__99_backcover_ru" />
                    </div>
                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>