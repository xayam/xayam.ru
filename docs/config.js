// config.js: файл настроек ресурса

// DOMAIN: домен ресурса
let DOMAIN = "xayam.ru";

let RU = "ru";
let EN = "en";

// LANGUAGES: поддерживаемые ресурсом языки
let LANGUAGES = Array(RU, EN);

// PATH: путь к основному js-файлу данных ресурса
let PATH = "res/data.js";

// CONFIG: вся конфигурация ресурса в одной переменной
let CONFIG = Array();
CONFIG["DOMAIN"] = DOMAIN;
CONFIG["LANGUAGES"] = LANGUAGES;
CONFIG["PATH"] = PATH;

// console.log: вывод конфигурации в консоль
console.log("[INFO] Configuration resource: ");
console.log(CONFIG);
