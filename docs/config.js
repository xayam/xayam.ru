// config.js: файл настроек

// DOMAIN: домен сайта
let DOMAIN = "xayam.ru";

let RU = "ru";
let EN = "en";

// LANGUAGES: поддерживаемые сайтом языки
let LANGUAGES = Array(RU, EN);

// DATA: путь к основному js-файлу данных сайта
let DATA = "res/data.js";

// CONFIG: вся конфигурация ресурса в одной переменной
let CONFIG = Array();
CONFIG["DOMAIN"] = DOMAIN;
CONFIG["LANGUAGES"] = LANGUAGES;
CONFIG["DATA"] = DATA;

// console.log: вывод конфигурации в консоль
console.log("[INFO] Configuration resource: ");
console.log(CONFIG);
