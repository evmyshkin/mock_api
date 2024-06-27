const {
    entityPaths
} = require("./paths");

const requestHandler = (app) => {
    const responseSets = {};

    const createHandlers = (receiverPath, mockPath, confirmPath) => {
        responseSets[receiverPath] = [];

        // Задать ответ заглушки
        app.post(receiverPath, (request, response) => {
            responseSets[receiverPath] = request.body;
            const res = {
                info: "Ответ заглушки задан",
                mockResponse: responseSets[receiverPath]
            };
            response.send(res);
        });

        // Прочитать текущий ответ из заглушки
        app.get(mockPath, (request, response) => {
            const res = responseSets[receiverPath];
            response.send(res);
        });

        // Очистить текущий ответ заглушки (Конфирм)
        app.post(confirmPath, (request, response) => {

            responseSets[receiverPath] = [];

            // const res = {
            //     info: "Ответ заглушки очищен",
            //     mockResponse: responseSets[receiverPath]
            // };
            response.send();
        });
    };

    entityPaths.forEach(({ receiverPath, mockPath, confirmPath }) => {
        createHandlers(receiverPath, mockPath, confirmPath);
    });
};

const generatorHandler = (app) => {

    // Сгенерировать все переменные
    app.post("/generate/allVariables", (request, response) => {

        const res =
        {
            "info": "Новые переменные окружения сгенерированы"
        };
        response.send(res);
    });


    // Сгенерировать AdFox и Креатив
    app.post("/generate/adfoxAndCreative", (request, response) => {

        const res =
        {
            "info": "Новые переменные AdFox и Креатива сгенерированы. Они привяжутся к Заявке по kvant_adv_campaign_source_id",
            "newVariables": ["kvant_adv_campaign_adfox_source_id", "kvant_line_number", "kvant_adfox_id", "kvant_creative_source_id", "kvant_creative_mt_name"]
        };
        response.send(res);
    });


    // Сгенерировать Статистику и Площадку
    app.post("/generate/statAndPad", (request, response) => {

        const res =
        {
            "info": "Новые переменные для Статистики и Площадки заданы. Они привяжутся к Креативу по creative_erir_token",
            "newVariables": ["gpmd_stat_source_id", "gpmd_stat_old_source_id", "gpmd_pad_random_id", "gpmd_pad_source_id", "gpmd_pad_referer_source_id", "gpmd_pad_site_name", "gpmd_site_url", "gpmd_pad_url", "sma_adfox_site_id"]
        };
        response.send(res);
    });
}

module.exports = {
    requestHandler,
    generatorHandler
};
