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