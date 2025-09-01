// data.js: файл данных ресурса

let site = "site";
let menu = "menu";

let menu_shop = "shop";
let menu_standards = "standards";
let menu_files = "files";
let menu_others = "others";
let menu_aboutus = "aboutus";
let menu_search = "search";

let menus = Array(
    menu_shop, menu_standards, menu_files,
    menu_others, menu_aboutus, menu_search,
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

CONFIG[menu][menu_shop][section_shop_chess] = Array(
    chesses,
);


CONFIG[menu][menu_standards] = Array();
