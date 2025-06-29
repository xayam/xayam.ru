<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
    <xsl:template match="/config">
        <html lang="ru">
            <head>
                <title>123</title>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <meta content="text/html; charset=utf-8" http-equiv="Content-type"/>
                <meta name="robots" content="INDEX,FOLLOW"/>
                <link rel="shortcut icon" href="favicon.ico" type="image/x-icon"/>
                <link rel="stylesheet" href="res/style.css"/>
            </head>
            <body>
                <div id="header">
                    <div id="logo">
                        <a href="#">XAYAM.RU</a> ::
                        <a href="#ru.catalog">RU</a> |
                        <a href="#en.catalog">EN</a>
                    </div>
                    <div id="slogan">
                        <i>Больше чем одна игра - больше чем одна форма...</i>
                    </div>
                </div>
                <div id="content">
                    <xsl:apply-templates select="document('index.xml')"/>
                </div>
                <div id="footer">
                    &#169; xayam 2025
                </div>
            </body>
        </html>
    </xsl:template>

</xsl:stylesheet>