<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
    <xsl:include href="include.xsl" />
    <xsl:template match="/root">
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
                <link rel="shortcut icon" href="{$favicon}" type="image/x-icon"/>
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
                <div id="map">
                    <span><h2>Карта сайта</h2></span>
                    <br />
                    <xsl:for-each select="$map">
                        <xsl:variable name="outer-id" select="./id" />
                        <xsl:variable name="title" select="./description/annotation/ru" />
                        <h3>
                            <a href="x/xmap/{$outer-id}" title="{$title}">
                                <div class="menu_level1">
                                    <xsl:value-of select="./description/name/ru" />
                                </div>
                            </a>
                        </h3>
                        <xsl:for-each select="document(concat('xmap/', ./id, '/menu.xml'))/menu//item">
                            <h4>
                                <a href="#ru/{$outer-id}/{./id}">
                                    <div class="menu_level2">
                                        <xsl:value-of select="./ru" />
                                    </div>
                                </a>
                            </h4>
                        </xsl:for-each>
                    </xsl:for-each>
                </div>
                <div id="content">
                    <xsl:for-each select="$map">
                        <xsl:variable name="outer-id" select="./id" />
                        <xsl:variable name="title" select="./description/annotation/ru" />
                        <h2>
                            <div class="menu_level1">
                                <xsl:value-of select="./description/name/ru" />
                            </div>
                        </h2>
                        <xsl:for-each select="document(concat('xmap/', ./id, '/menu.xml'))/menu//item">
                            <a name="ru/{$outer-id}/{./id}" />
                            <h3>
                                <div class="menu_level2">
                                    <xsl:value-of select="./ru" />
                                </div>
                            </h3>
                            <xsl:copy-of select="document(
                                        concat('xmap/', $outer-id, '/', ./id, '/content.xml'))/content/ru/*" />
                        </xsl:for-each>
                    </xsl:for-each>
                </div>
                <div id="footer">
                    <xsl:value-of select="$footer" />
                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>