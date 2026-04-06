<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
    <xsl:variable name="s02_with_dice_ru" select="'Часть 3. Игры с костями'" />
    <xsl:variable name="s02_with_dice__01_dice_chess_ru" select="document('01-dice-chess/ru.xml')/ru/div" />
    <xsl:variable name="s02_with_dice__02_random_chess_ru" select="document('02-random-chess/ru.xml')/ru/div" />
    <xsl:variable name="s02_with_dice__03_chess_with_d12_ru" select="document('03-chess-with-D12/ru.xml')/ru/div" />
    <xsl:variable name="s02_with_dice__04_chess_with_3xd12_ru" select="document('04-chess-with-3xD12/ru.xml')/ru/div" />
    <xsl:variable name="s02_with_dice__05_random_other_ru" select="document('05-random-other/ru.xml')/ru/div" />
</xsl:stylesheet>