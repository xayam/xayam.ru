<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
    <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
    <xsl:template name="block-body">
        <div id="chessboard">1</div>
        <div class="left">
            <div class="menus">
                <label for="select_menu">Выберите режим:</label>
                <select id="select_menu" name="select_menu" class="select_menu">
                    <option value="mode_u_vs_ai_level_1">Пользователь против AI (Уровень 1)</option>
                    <option value="mode_u_vs_ai_level_2">Пользователь против AI (Уровень 2)</option>
                    <option value="mode_u_vs_ai_level_3">Пользователь против AI (Уровень 3)</option>
                    <option value="mode_ai_vs_u_level_1">AI (Уровень 1) против Пользователя</option>
                    <option value="mode_ai_vs_u_level_2">AI (Уровень 2) против Пользователя</option>
                    <option value="mode_ai_vs_u_level_3">AI (Уровень 3) против Пользователя</option>
                    <option value="mode_u1_vs_u2">Пользователь 1 против Пользователя 2</option>
                    <option value="mode_ai_vs_ai_level_1">AI (Уровень 1) против AI (Уровень 1)</option>
                    <option value="mode_ai_vs_ai_level_2">AI (Уровень 2) против AI (Уровень 2)</option>
                    <option value="mode_ai_vs_ai_level_3">AI (Уровень 3) против AI (Уровень 3)</option>
                </select>
            </div>
            <div class="games">
                <label for="select_game">Выберите игру:</label>
                <select id="select_game" name="select_game" class="select_game">
                    <xsl:variable name="parts" select="document('../rules/ru-parts.xml')/parts/part" />
                    <xsl:for-each select="$parts">
                        <xsl:variable name="number" select="number" />
                        <xsl:variable name="id" select="id" />
                        <xsl:variable name="name" select="name" />
                        <xsl:variable name="games"
                                      select="document(concat('../rules/', $number, '-', $id, '/ru-games.xml'))/games/game"/>
                        <xsl:variable name="subname"
                                      select="substring-after($name, '. ')" />
                        <xsl:if test="$number!='00' and $number!='99'">
                            <optgroup label="{$subname}">
                                <xsl:for-each select="$games">
                                    <xsl:variable name="number2" select="number" />
                                    <xsl:variable name="id2" select="id" />
                                    <xsl:variable name="name2" select="name" />
                                    <xsl:variable name="gambling2" select="gambling" />
                                    <xsl:if test="$gambling2='true'">
                                        <option value="{$id2}">
                                            <xsl:value-of select="$name2" />
                                        </option>
                                    </xsl:if>
                                </xsl:for-each>
                            </optgroup>
                        </xsl:if>
                    </xsl:for-each>
                </select>
            </div>
            <div class="rules">
                <xsl:variable name="parts2" select="document('../rules/ru-parts.xml')/parts/part" />
                <xsl:for-each select="$parts2">
                    <xsl:variable name="number" select="number" />
                    <xsl:variable name="id" select="id" />
                    <xsl:variable name="name" select="name" />
                    <xsl:variable name="games"
                                  select="document(concat('../rules/', $number, '-', $id, '/ru-games.xml'))/games/game"/>
                    <xsl:for-each select="$games">
                        <xsl:variable name="number2" select="number" />
                        <xsl:variable name="id2" select="id" />
                        <xsl:variable name="name2" select="name" />
                        <xsl:variable name="gambling2" select="gambling" />
                        <xsl:if test="$gambling2='true'">
                            <xsl:variable name="content"
                                      select="document(concat('../rules/', $number, '-', $id, '/', $number2, '-', $id2, '/ru.xml'))/ru/div"/>
                            <xsl:choose>
                                <xsl:when test="$id2='chess'">
                                    <div id="rules_{$id2}" class="rules_game active">
                                        <xsl:copy-of select="$content" />
                                    </div>
                                </xsl:when>
                                <xsl:otherwise>
                                    <div id="rules_{$id2}" class="rules_game">
                                        <xsl:copy-of select="$content" />
                                    </div>
                                </xsl:otherwise>
                            </xsl:choose>
                        </xsl:if>
                    </xsl:for-each>
                </xsl:for-each>
            </div>
        </div>
        <div class="board">
        </div>
    </xsl:template>

    <xsl:template match="/">
        <html lang="ru">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport"
                  content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0"/>
            <meta http-equiv="X-UA-Compatible" content="ie=edge" />
            <title>Варианты шахмат на площадке от XAYAM.RU</title>
            <style>
                <xsl:variable name="css" select="/root/css/item" />
                <xsl:for-each select="$css">
                    {{{<xsl:value-of select="."/>}}}
                </xsl:for-each>
            </style>
        </head>
        <body>
            <xsl:variable name="js" select="/root/js/item" />
            <xsl:for-each select="$js">
                <script>
                   {{{<xsl:value-of select="."/>}}}
                </script>
            </xsl:for-each>
            <xsl:call-template name="block-body"/>
        </body>
        </html>
    </xsl:template>
</xsl:stylesheet>