
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function deepClone(obj) {
    if (obj === null || typeof obj !== 'object') return obj;
    if (obj instanceof Date) return new Date(obj);
    if (obj instanceof Array) return obj.map(item => deepClone(item));
    if (obj instanceof Object) {
        return Object.keys(obj).reduce((acc, key) => {
            acc[key] = deepClone(obj[key]);
            return acc;
        }, {});
    }
    return obj;
}
