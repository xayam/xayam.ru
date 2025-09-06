<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>

    <xsl:variable name="lowercase" select="'abcdefghijklmnopqrstuvwxyz'" />
    <xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'" />

    <xsl:variable name="domain"    select="document('config.xml')/config/domain" />

<!--    <xsl:variable name="ru"        select="translate(document('config.xml')/config/languages/ru, $lowercase, $uppercase)" />-->
<!--    <xsl:variable name="en"        select="translate(document('config.xml')/config/languages/en, $lowercase, $uppercase)" />-->

    <xsl:variable name="slogan_ru" select="document('config.xml')/config/slogan/ru" />
    <xsl:variable name="slogan_en" select="document('config.xml')/config/slogan/en" />

    <xsl:variable name="header_ru" select="document('config.xml')/config/header/ru//subheader" />
    <xsl:variable name="header_en" select="document('config.xml')/config/header/en//subheader" />

</xsl:stylesheet>