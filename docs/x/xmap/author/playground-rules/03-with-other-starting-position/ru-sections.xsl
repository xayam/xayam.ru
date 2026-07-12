<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
    <xsl:variable name="s03_other_start_ru" select="'Часть 4. Игры с другой стартовой позицией'" />
    <xsl:variable name="s03_other_start__01_chess_960_ru" select="document('01-chess-960/ru.xml')/ru/div" />
    <xsl:variable name="s03_other_start__02_DFRC_ru" select="document('02-DFRC/ru.xml')/ru/div" />
    <xsl:variable name="s03_other_start__03_racing_kings_ru" select="document('03-racing-kings/ru.xml')/ru/div" />
    <xsl:variable name="s03_other_start__04_bad_chess_ru" select="document('04-really-bad-chess/ru.xml')/ru/div" />
</xsl:stylesheet>