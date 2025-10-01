<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>

    <xsl:variable name="favicon" select="document('config.xml')/config/favicon" />

    <xsl:variable name="lowercase" select="'abcdefghijklmnopqrstuvwxyz'" />
    <xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'" />

    <xsl:variable name="domain"    select="document('config.xml')/config/domain" />

    <xsl:variable name="ru"        select="document('config.xml')/config/languages/ru" />
    <xsl:variable name="en"        select="document('config.xml')/config/languages/en" />

    <xsl:variable name="slogan_ru" select="document('config.xml')/config/slogan/ru" />
    <xsl:variable name="slogan_en" select="document('config.xml')/config/slogan/en" />

    <xsl:variable name="header_ru" select="document('config.xml')/config/header/ru//subheader" />
    <xsl:variable name="header_en" select="document('config.xml')/config/header/en//subheader" />

    <xsl:variable name="footer" select="document('config.xml')/config/footer" />

    <xsl:variable name="map" select="document('xmap/map.xml')/map//item" />

</xsl:stylesheet>