<?xml version="1.0" encoding="utf-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
    <xsl:template match="/">
        <xsl:variable name="lowercase" select="'abcdefghijklmnopqrstuvwxyz'" />
        <xsl:variable name="uppercase" select="'ABCDEFGHIJKLMNOPQRSTUVWXYZ'" />
        <html lang="ru">
            <head>
                <title>
                    <xsl:value-of
                            select="translate(index/config/domain, $lowercase, $uppercase)" /> ::
                    <xsl:value-of select="index/data/site/slogan/ru" />
                </title>
                <meta charset="UTF-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
                <meta content="text/html; charset=utf-8" http-equiv="Content-type"/>
                <meta name="robots" content="INDEX,FOLLOW"/>
                <link rel="shortcut icon" href="favicon.ico" type="image/x-icon"/>
                <link rel="stylesheet" href="res/style.css"/>
            </head>
            <body>
                <script>
                    let domain = "&lt;xsl:value-of select='index/config/domain' />";
                    let title = '';
                </script>
                <div id="header">
                    <div id="logo">
                        <a id="logo_domain" href="#ru.catalog">
                            <xsl:value-of
                                    select="translate(index/config/domain, $lowercase, $uppercase)" />
                        </a> ::
                        <a href="#ru.catalog">
                            <xsl:value-of
                                    select="translate(index/config/languages/ru, $lowercase, $uppercase)" />
                        </a> |
                        <a href="#en.catalog">
                            <xsl:value-of
                                    select="translate(index/config/languages/en, $lowercase, $uppercase)" />
                        </a>
                    </div>
                    <div id="slogan">
                        <i>
                            <xsl:value-of select="index/data/site/slogan/ru" />
                        </i>
                    </div>
                </div>
                <div id="content">
                    <ul>
                        <li><h2>Продаю</h2>
                            <a href="https://www.ozon.ru/seller/xayam-ru-2439849" target="blank">Магазин xayam.ru на ОЗОН</a><br />
                            <h3>На Авито</h3>
                            <a href="https://www.avito.ru/moskva/rezume/programmist_python_udalenno_4298167970" target="blank">Программист Python удаленно</a><br />
                            <a href="https://www.avito.ru/moskva/knigi_i_zhurnaly/obmen_kniga_na_knigu_4298533297" target="blank">Обмен книга на книгу бесплатно</a><br />
                            <a href="https://www.avito.ru/moskva/tovary_dlya_kompyutera/adapter_nvme_pcie_pci-e_x16_dlya_m.2_m_key_4_ssd_ra_7401015422" target="blank">Адаптер nvme PCIe PCI-E X16 для M.2 M Key 4 SSD</a><br />
                            <a href="https://www.avito.ru/moskva/odezhda_obuv_aksessuary/dublenka_naturalnaya_muzhskaya_52-ogo_razmera_3785629125" target="blank">Дубленка натуральная мужская 52-ого размера</a><br />
                            <a href="https://www.avito.ru/moskva/odezhda_obuv_aksessuary/norkovaya_shuba_48_razmer_3786394684" target="blank">Норковая шуба 48 размер</a><br />
                        </li>
                        <li><h2>Другое</h2>
                            Здесь <a href="others">./others</a> Вы можете найти различную информацию, храняющуюся на этом сайте. <br />Здесь <a href="rewlis/index.html">./rewlis</a> находится демо проекта REWLIS - плеер, реализующий концепцию <br />RWL - "Read While you Listen" - "Читай пока слушаешь".
                        </li>
                        <li><h2>Основатель</h2>
                            Телеграм: <a href="https://t.me/AlekseyBelyanin" target="blank">@AlekseyBelyanin</a><br />
                            Почта: <a href="mailto:xayam@yandex.ru">xayam@yandex.ru</a><br />
                            Портфолио-бот: <a href="https://t.me/xPortfoliosBot" target="blank">https://t.me/xPortfoliosBot</a>
                        </li>
                    </ul>
                </div>
                <div id="footer">
                    &#169; xayam 2025
                </div>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>