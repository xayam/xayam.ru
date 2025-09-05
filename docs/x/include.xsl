<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
    <xsl:variable name="lowercase" select="'abcdefghijklmnopqrstuvwxyz'" />
    <xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'" />
    <xsl:variable name="domain"    select="translate(config/domain,       $lowercase, $uppercase)" />
    <xsl:variable name="ru"        select="translate(config/languages/ru, $lowercase, $uppercase)" />
    <xsl:variable name="en"        select="translate(config/languages/en, $lowercase, $uppercase)" />
    <xsl:variable name="slogan_ru" select="document('site.xml')/site/slogan/ru" />
    <xsl:variable name="slogan_en" select="document('site.xml')/site/slogan/en" />
    <xsl:variable name="header_ru" select="document('site.xml')/site/header/ru//subheader" />
    <xsl:variable name="header_en" select="document('site.xml')/site/header/en//subheader" />
</xsl:stylesheet>