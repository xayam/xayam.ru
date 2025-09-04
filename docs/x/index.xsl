<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
    <xsl:template match="/root">
        <xsl:variable name="lowercase" select="'abcdefghijklmnopqrstuvwxyz'" />
        <xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'" />
		<xsl:variable name="domain"    select="translate(config/domain,       $lowercase, $uppercase)" />
        <xsl:variable name="ru"        select="translate(config/languages/ru, $lowercase, $uppercase)" />
        <xsl:variable name="en"        select="translate(config/languages/en, $lowercase, $uppercase)" />
        <xsl:variable name="slogan_ru" select="document('site.xml')/site/slogan/ru" />
        <xsl:variable name="slogan_en" select="document('site.xml')/site/slogan/en" />
        <xsl:variable name="header_ru" select="document('site.xml')/site/header/ru/*" />
        <xsl:variable name="header_en" select="document('site.xml')/site/header/en/*" />
        <html lang="ru">
            <head>
                <title>
                    <xsl:value-of select="$domain" /> ::
                    <xsl:value-of select="$slogan_ru" />
                </title>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <meta content="text/html; charset=utf-8" http-equiv="Content-type"/>
                <meta name="robots" content="INDEX,FOLLOW"/>
                <link rel="shortcut icon" href="favicon.ico" type="image/x-icon"/>
                <link rel="stylesheet" href="x/xstyle/resources/default.css"/>
                <link rel="stylesheet" href="x/xstyle/resources/style.css"/>
            </head>
            <body>
                <div id="header">
                    <xsl:for-each select="$header_ru">
                        <span>
                            <a href="{@href}">
                                <xsl:value-of select="." />
                            </a>
                        </span>
                    </xsl:for-each>
                </div>
                <div id="content">
                    
                </div>
                <div id="footer">
                    &#169; xayam 2025
                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>