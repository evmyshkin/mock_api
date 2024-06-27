const entityPaths = [
    {
        // Квант Заявка
        receiverPath: "/receiver/v0.1/mt_request/updated",
        mockPath: "/v0.1/mt_request/updated",
        confirmPath: "/v0.1/mt_request/event/confirmed"
    },
    {
        // Квант Строка Заявки AdFox
        receiverPath: "/receiver/v0.1/mt_requestdetail/updated",
        mockPath: "/v0.1/mt_requestdetail/updated",
        confirmPath: "/v0.1/mt_requestdetail/event/confirmed",
    },
    {
        // Квант Рекламный Материал
        receiverPath: "/receiver/v0.1/mt_advertmaterial/updated",
        mockPath: "/v0.1/mt_advertmaterial/updated",
        confirmPath: "/v0.1/mt_advertmaterial/event/confirmed"
    },
    {
        // Квант Изначальный Договор
        receiverPath: "/receiver/v0.1/mt_originalcontract/updated",
        mockPath: "/v0.1/mt_originalcontract/updated",
        confirmPath: "/v0.1/mt_originalcontract/event/confirmed"
    },
    {
        // СМА Рекламная Кампания
        receiverPath: "/receiver/v1/advCampaign/updated",
        mockPath: "/v1/advCampaign/updated",
        confirmPath: "/v1/advCampaign/event/confirmed"
    },
    {
        // СМА Заказ на Размещение
        receiverPath: "/receiver/v1/order/updated",
        mockPath: "/v1/order/updated",
        confirmPath: "/v1/order/event/confirmed"
    },
    {
        // СМА Изначальный Договор
        receiverPath: "/receiver/v1/initialContract/updated",
        mockPath: "/v1/initialContract/updated",
        confirmPath: "/v1/initialContract/event/confirmed"
    },
    {
        // СМА Доходный Договор
        receiverPath: "/receiver/v1/contractDocument/updated",
        mockPath: "/v1/contractDocument/updated",
        confirmPath: "/v1/contractDocument/event/confirmed"
    },
    {
        // СМА Акт
        receiverPath: "/receiver/v1/act/updated",
        mockPath: "/v1/act/updated",
        confirmPath: "/v1/act/event/confirmed"
    },
    {
        // СМА Размещение Факт
        receiverPath: "/receiver/v1/factPlacement/updated",
        mockPath: "/v1/factPlacement/updated",
        confirmPath: "/v1/factPlacement/event/confirmed"
    },
    {
        // СМА Расходный Договор
        receiverPath: "/receiver/v1/platformContract/updated",
        mockPath: "/v1/platformContract/updated",
        confirmPath: "/v1/platformContract/event/confirmed"
    },
    {
        // СМА Канал
        receiverPath: "/receiver/v1/platform/updated",
        mockPath: "/v1/platform/updated",
        confirmPath: "/v1/platform/event/confirmed"
    }
]

module.exports = {
    entityPaths
};