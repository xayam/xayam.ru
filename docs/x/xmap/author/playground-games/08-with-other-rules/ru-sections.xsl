<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
    <xsl:variable name="s01_classic_games_ru" select="'Классические игры'" />
    <xsl:variable name="s01_classic_games__01_chess_ru" select="document('01-chess/ru.xml')/ru/div" />
    <xsl:variable name="s01_classic_games__02_checkers_ru" select="document('02-checkers/ru.xml')/ru/div" />
</xsl:stylesheet>