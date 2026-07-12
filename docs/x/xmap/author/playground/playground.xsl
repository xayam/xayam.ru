<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
    <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
    <xsl:template name="block-body">
        <div id="chessboard">1</div>
        <div class="left">
            <div class="games_list">
                <select name="game_input" class="game_input">
                    <option value="chess" selected="selected">Шахматы</option>
                    <option value="dicechess">ДайсЧес</option>
                    <option value="crazyhouse">КрейзиХаус</option>
                </select>
            </div>
            <div class="game_rules">
                123
            </div>
        </div>
        <div class="center">
            <div class="board_center">

            </div>
        </div>
        <div class="right">

        </div>
        <script type="text/javascript">
            {{{PG_THREE_CORE_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_THREE_MODULE_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_JQUERY_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_CHESSBOARD_JS}}}
        </script>

        <script type="text/javascript">
            {{{PG_UTILS_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_MATERIAL_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_GEOMETRY_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_BOARD_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_FIGURE_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_CAMERA_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_SCENE_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_KEYBOARD_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_MOUSE_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_TOUCHE_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_ACTION_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_EVENT_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_UCI_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_COMMAND_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_RULE_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_GAME_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_USER_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_ENGINE_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_EVALUATE_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_SEARCH_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_AI_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_STATE_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_CONFIG_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_APP_JS}}}
        </script>
        <script type="text/javascript">
            {{{PG_LOAD_JS}}}
        </script>
    </xsl:template>
    <xsl:template match="/">
        <html lang="ru">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport"
                  content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0"/>
            <meta http-equiv="X-UA-Compatible" content="ie=edge" />
            <title>PlayGround by Xayam</title>
            <style>
                {{{PG_CHESSBOARD_CSS}}}

                {{{PG_DEFAULT_CSS}}}

                {{{PG_LAYOUT_CSS}}}
            </style>
        </head>
        <body>
              <xsl:call-template name="block-body"/>
        </body>
        </html>
    </xsl:template>
</xsl:stylesheet>