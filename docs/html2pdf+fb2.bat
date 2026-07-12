@echo off

D:\Programs\WeasyPrint\weasyprint.exe E:\Xayam\XWork\XWorker\Projects\xarchive\XArchive\subprojects\org\xayam.ru\xayam.ru\docs\x\xmap\author\playground-games\ru-book.pdf.html E:\Xayam\XWork\XWorker\Projects\xarchive\XArchive\subprojects\org\xayam.ru\xayam.ru\docs\x\xmap\\author\playground-games\ru-book.pdf

D:\Programs\Calibre\Calibre\ebook-convert.exe E:\Xayam\XWork\XWorker\Projects\xarchive\XArchive\subprojects\org\xayam.ru\xayam.ru\docs\x\xmap\author\playground-games\ru-book.html E:\Xayam\XWork\XWorker\Projects\xarchive\XArchive\subprojects\org\xayam.ru\xayam.ru\docs\x\xmap\\author\playground-games\ru-book.epub --no-default-epub-cover --preserve-cover-aspect-ratio --smarten-punctuation

D:\Programs\Calibre\Calibre\ebook-convert.exe E:\Xayam\XWork\XWorker\Projects\xarchive\XArchive\subprojects\org\xayam.ru\xayam.ru\docs\x\xmap\author\playground-games\ru-book.epub E:\Xayam\XWork\XWorker\Projects\xarchive\XArchive\subprojects\org\xayam.ru\xayam.ru\docs\x\xmap\\author\playground-games\ru-book.fb2 --level1-toc="//h:h1" --page-breaks-before="//*[name()='h1']"

pause