<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
    <xsl:variable name="title_ru" select="/book/title/ru" />

    <xsl:include href="00-begin/ru-sections.xsl" />
    <xsl:include href="01-classic-games/ru-sections.xsl" />
</xsl:stylesheet>