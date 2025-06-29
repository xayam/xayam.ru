// data.js: файл данных ресурса

let site = "site";
let menu = "menu";

let section_shop = "shop";
let section_standards = "standards";
let section_files = "files";
let section_others = "others";
let section_aboutus = "aboutus";
let section_search = "search";

let sections = Array(
    section_shop, section_standards, section_files,
    section_others, section_aboutus, section_search,
);

CONFIG[site]["slogan"][RU] = "Больше чем одна игра - больше чем одна форма...";
CONFIG[site]["slogan"][EN] = "More then one game - more then one form...";

CONFIG[site]["title"][RU] = DOMAIN + " :: " + CONFIG[site]["slogan"][RU];
CONFIG[site]["title"][EN] = DOMAIN + " :: " + CONFIG[site]["slogan"][EN];

// ...

let section_shop_chess = "chess";
let chesses = Array();
chesses["1000010"]["images"] = Array(
    "res/shop/chesses/1000010/0.jpg",
    "res/shop/chesses/1000010/1.jpg",
    "res/shop/chesses/1000010/2.jpg",
);
chesses["1000010"][RU] = "русский 1000010";
chesses["1000010"][EN] = "english 1000010";

CONFIG[menu][section_shop][section_shop_chess] = Array(chesses, );


CONFIG[menu][section_standards] = Array();
