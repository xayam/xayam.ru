<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
    <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
    <xsl:include href="ru-include.xsl" />
    <xsl:template name="block-booker">
        <div id="booker">
            <xsl:variable name="parts" select="document('ru-parts.xml')/parts/part" />
            <xsl:for-each select="$parts">
                <xsl:variable name="number" select="number" />
                <xsl:variable name="id" select="id" />
                <xsl:variable name="name" select="name" />
                <xsl:variable name="games" select="document(concat($number, '-', $id, '/ru-games.xml'))/games/game"/>
                <div id="section-{$number}">
                    <xsl:if test="$number!='00'">
                        <br />
                        <div class="page-break">
                        </div>
                        <a name="part_{$number}" />
                        <a href="#_part_{$number}">
                            <h1><xsl:value-of select="$name" /></h1>
                        </a>
                    </xsl:if>
                    <xsl:for-each select="$games">
                        <xsl:variable name="number2" select="number" />
                        <xsl:variable name="id2" select="id" />
                        <xsl:variable name="name2" select="name" />
                        <xsl:variable name="content"
                                      select="document(concat($number, '-', $id, '/', $number2, '-', $id2, '/ru.xml'))/ru/div"/>
                        <xsl:if test="$name2!=' '">
                            <br />
                            <a name="{$id2}" id="{$id2}" />
                            <a href="#_{$id2}">
                                <h1><xsl:value-of select="$name2" /></h1>
                            </a>
                        </xsl:if>
                        <xsl:if test="$content[@class='table']">
                            <xsl:for-each select="$parts">
                                <xsl:variable name="number3" select="number" />
                                <xsl:variable name="id3" select="id" />
                                <xsl:variable name="name3" select="name" />
                                <xsl:variable name="games2" select="document(concat($number3, '-', $id3, '/ru-games.xml'))/games/game"/>
                                <xsl:if test="$number3='04' or $number3='08'">
                                    <div class="page-break">
                                    </div>
                                </xsl:if>
                                <xsl:if test="$number3!='00'">
                                    <br />
                                    <a name="_part_{$number3}" />
                                    <p class="section">
                                        <a href="#part_{$number3}">
                                            <xsl:value-of select="$name3" />
                                        </a>
                                    </p>
                                    <br />
                                </xsl:if>
                                <xsl:for-each select="$games2">
                                    <xsl:variable name="number4" select="number" />
                                    <xsl:variable name="id4" select="id" />
                                    <xsl:variable name="name4" select="name" />
                                    <xsl:if test="$name4!=' '">
                                        <a name="_{$id4}" />
                                        <p class="subsection">
                                            <a href="#{$id4}" class="counter">
                                                <xsl:value-of select="$name4" />
                                            </a>
                                        </p>
                                        <br />
                                    </xsl:if>
                                </xsl:for-each>
                            </xsl:for-each>
                            <div class="page-break">
                            </div>
                        </xsl:if>
                        <xsl:copy-of select="$content" />
                    </xsl:for-each>
                </div>
            </xsl:for-each>
        </div>
    </xsl:template>

    <xsl:template match="/">
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
                <style>
                    {{{XGAME_DEFAULT_CSS}}}

                    {{{XGAME_STYLE_CSS}}}
                </style>
                <xsl:if test="$book_type='pdf'">
                    <script>
                        {{{XGAME_PAGED}}}
                    </script>
                </xsl:if>
            </head>
            <body>
                <xsl:call-template name="block-booker"/>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>