<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
    <xsl:include href="ru-include.xsl" />
    <xsl:template match="/book">
        <html lang="ru">
            <head>
                <title>
                    <xsl:value-of select="$title_ru" />
                </title>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <meta content="text/html; charset=utf-8" http-equiv="Content-type"/>
                <meta name="robots" content="INDEX,FOLLOW"/>
                <link rel="shortcut icon" href="favicon.ico" type="image/x-icon"/>
                <link rel="stylesheet" href="xbook.xgame/resources/default.css"/>
                <link rel="stylesheet" href="xbook.xgame/resources/style.css"/>
            </head>
            <body>
                <div id="book">
                    <div id="section-00">
                        <xsl:copy-of select="$s00_begin__01_cover_ru" />
                    </div>
                    <div id="section-01">
                        <h1>Классические игры</h1>

                    </div>
                </div>

            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>