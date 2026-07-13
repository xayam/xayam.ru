<xsl:stylesheet version="1.0" xmlns:xsl='http://www.w3.org/1999/XSL/Transform'>
    <xsl:output method="xml" indent="yes" encoding="UTF-8"/>
    <xsl:template match="/">
        <FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" xmlns:l="http://www.w3.org/1999/xlink">
        <description>
            <title-info>
                <genre>prose_classic</genre>
                <author>
                    <first-name>Пол</first-name>
                    <last-name>Андерсън</last-name>
                </author>
                <book-title>Операция „Хаос“</book-title>

                <keywords>Научна фантастика</keywords>
                <coverpage>
                    <image l:href="#img_1-1"/>
                </coverpage>
                <lang>bg</lang>
                <src-lang>en</src-lang>
                <translator>
                    <first-name> </first-name>
                    <last-name> </last-name>
                </translator>
                <sequence name="Стивън Матучек" number="1"/>
            </title-info>
            <src-title-info>
                <genre>prose_classic</genre>
                <author>
                    <first-name>Poul</first-name>
                    <middle-name>William</middle-name>
                    <last-name>Anderson</last-name>
                </author>
                <book-title></book-title>
                <date>1971</date>
                <lang>en</lang>
                <sequence name="Steven Matuchek" number="1"/>
            </src-title-info>
            <document-info>
                <author>
                    <nickname>(неизвестен автор)</nickname>
                </author>
                <program-used>Mylib SfbToFb2 Converter</program-used>
                <date>2010-07-07 06:06:52</date>
                <id>http://chitanka.info/text/548</id>
                <version>0.2</version>
                <history>
                    <p>0.1 (2006-08-10) — Добавяне</p>
                    <p>0.2 (2006-08-11 10:16:11) — Корекция</p>
                </history>
            </document-info>
        </description>
    </xsl:template>

</xsl:stylesheet>