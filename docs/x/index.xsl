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
                <div id="content">
                    <xsl:for-each select="$map">
                        <div class="menu_level1">
                            <xsl:variable name="outer-id" select="./id" />
                            <a href="#ru/{$outer-id}">
                                <xsl:value-of select="./ru" />
                            </a>
                            <div class="menu_level2">
                                <xsl:for-each select="document(concat('xmap/', ./id, '/menu.xml'))/menu//item">
                                    <a href="#ru/{$outer-id}/{./id}">
                                        <xsl:value-of select="./ru" />
                                    </a>
                                    <br />
                                </xsl:for-each>
                            </div>
                        </div>
                    </xsl:for-each>
                </div>
                <div id="footer">
                    <xsl:value-of select="$footer" />
                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>