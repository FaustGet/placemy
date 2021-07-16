class office_type():
    value={
      "office":"Офис",
      "garage":"Гараж",
      "warehouse":"Склад",
      "premisessFreeAppointment":"Помещения свободного назначения",
       "smallArchitecturalForms":"Малые архитектурные формы",
       "productionPremises":"Производственное помещение",
       "shop":"Магазин",
       "restaurant":"Общепит",
       "salon":"Салон",
       "recreationСenter":"База отдыха",
       "healthСare":"Здравоохранение",
       "service":"Сервис",
       "sport":"Спорткомплекс"}

class ground_type():
    value={
        "farm":"Фермерское хоз-во",
        "subsidiaryFarm":"Личное подсобное хозяйство",
        "secondaryBuilding":"Садоводство",
        "individualСonstruction":"ИЖС",
        "industrialDestination":"Земля промназначения",
        "nonProfitPartnership":"ДНП"
    }

class deal_type():
    value = {
             "sell":"Продажа",
             "rent_long":"Аренда",
             "rent_mount":"посуточная аренда"
            }

class building_type():
    value = {
             "secondaryBuilding":"Вторичный рынок",
             "newBuilding":"Новостройки"
            }
class building_renovation():
    value = {
             "cosmetic": "Косметический",
             "euro": "Евро",
             "design": "Дизайнерский",
             "without": "Без ремонта"
             }

class type_sell_data():
    value = {
             "freeSell":"Свободная продажа",
             "mortgage":"Возможна ипотека",
             "credit":"Возможен кредит"
             }

class for_who_data():
    value ={
            "any":"Любой",
            "family":"Семья",
            "woman":"Женщина",
            "man":"Мужчина"
            }

class type_objects():
    value = {
             "apartment":"Квартиру",
             "room":"Комнату",
             "house":"Дом",
             "ground":"Участок",
             "commercy":"Коммерческую",
             "building":"Здание"

            }
class city_type():
    value={
        'dushanbe': 'Душанбе',
        'Hudgan': 'Худжанд',
        'AburahmoniDzhomi': 'Абдурахмони Джоми',
        'Aini': 'Айни',
        'Asht': 'Ашт',
        'Baldzhuvan': 'Бальджуван',
        'BobdjonGafurov': 'Бободжон Гафуров',
        'Bohtar': 'Бохтар (Курган-Тюбе)',
        'Buston': 'Бустон (Чкаловск)',
        'Vanzh': 'Вандж',
        'Varzob': 'Варзоб',
        'Vahdat': 'Вахдат',
        'Vash': 'Вахш',
        'Vose': 'Восе',
        'Gissar': 'Гиссар',
        'GornayaMatcha': 'Горная Матча',
        'Guliston': 'Гулистон (Кайраккум)',
        'Dangara': 'Дангара',
        'Devashtich': 'Деваштич (Ганчи)',
        'DzhaborRasulov': 'Джаббор Расулов',
        'Dzhaihun': 'Джайхун (Кумсангир)',
        'DzhaloliddinaBalhi': 'Джалолиддина Балхи (Руми)',
        'Dzhami': 'Джами',
        'Dusti': 'Дусти (Джиликуль)',
        'Zafarbad': 'Зафарабад',
        'Istaravshan': 'Истаравшан',
        'Istiklol': 'Истиклол',
        'Isfara': 'Исфара',
        'Ishkamshim': 'Ишкашим',
        'Kabodien': 'Кабодиён',
        'Kanibadam': 'Канибадам',
        'Kulyab': 'Куляб',
        'Kushonien': 'Кушониён (Бохтар)',
        'Lahsh': 'Лахш (Джиргиталь)', 'Levakand': 'Леваканд (Сарбанд)',
        'Matcha': 'Матча',
        'Muminabad': 'Муминабад',
        'Murgab': 'Мургаб',
        'Nosiri Husrav': 'Носири Хусрав',
        'Nurabad': 'Нурабад',
        'Nurek': 'Нурек',
        'Pendjakent': 'Пенджикент',
        'Pyandzh': 'Пяндж',
        'Rasht': 'Рашт',
        'Rogun': 'Рогун',
        'Roshtkala': 'Рошткала',
        'Rudaki': 'Рудаки',
        'Rushan': 'Рушан',
        'Sangvor': 'Сангвор (Тавильдара)',
        'Spitamen': 'Спитамен',
        'Tadzhikabad': 'Таджикабад',
        'Temurmalik': 'Темурмалик',
        'Tursunzade': 'Турсунзаде',
        'Faizabad': 'Файзабад',
        'Farhor': 'Фархор',
        'Hamadani': 'Хамадани',
        'Hovaling': 'Ховалинг',
        'Horog': 'Хорог',
        'Huroson': 'Хуросон',
        'ShamsiddinShohin': 'Шамсиддин Шохин (Шуроабад)',
        'Shahrinav': 'Шахринав',
        'Shariston': 'Шахристон',
        'Shahritus': 'Шахритус',
        'Shugan': 'Шугнан',
        'Yavan': 'Яван'
    }
    options = {
        "options":[
        {
                "value":'dushanbe',
                "label": 'Душанбе'},
        {
                "value": 'Hudgan',
                "label":  'Худжанд'},
        {
                "value": 'AburahmoniDzhomi',
                "label":  'Абдурахмони Джоми'},
        {
                "value": 'Aini',
                "label":  'Айни'},
        {
                "value": 'Asht',
                "label":  'Ашт'},
        {
                "value": 'Baldzhuvan',
                "label":  'Бальджуван'},
        {
                "value": 'BobdjonGafurov',
                "label":  'Бободжон Гафуров'},
        {
                "value": 'Bohtar',
                "label":  'Бохтар (Курган-Тюбе)'},
        {
                "value": 'Buston',
                "label":  'Бустон (Чкаловск)'},
        {
                "value": 'Vanzh',
                "label":  'Вандж'},
        {
                "value": 'Varzob',
                "label":  'Варзоб'},
        {
                "value":  'Vahdat',
                "label":  'Вахдат'},
        {
                "value": 'Vash',
                "label":  'Вахш'},
        {
                "value": 'Vose',
                "label":  'Восе'},
        {
                "value": 'Gissar',
                "label":  'Гиссар'},
        {
                "value": 'GornayaMatcha',
                "label":  'Горная Матча'},
        {
                "value": 'Guliston',
                "label":  'Гулистон (Кайраккум)'},
        {
                "value": 'Dangara',
                "label":  'Дангара'},
        {
                "value": 'Devashtich',
                "label":  'Деваштич (Ганчи)'},
        {
                "value": 'DzhaborRasulov',
                "label":  'Джаббор Расулов'},
        {
                "value": 'Dzhaihun',
                "label":  'Джайхун (Кумсангир)'},
        {
                "value": 'DzhaloliddinaBalhi',
                "label":  'Джалолиддина Балхи (Руми)'},
        {
                "value": 'Dzhami',
                "label":  'Джами'},
        {
                "value": 'Dusti',
                "label":  'Дусти (Джиликуль)'},
        {
                "value": 'Zafarbad',
                "label":  'Зафарабад'},
        {
                "value": 'Istaravshan',
                "label":  'Истаравшан'},
        {
                "value": 'Istiklol',
                "label":  'Истиклол'},
        {
                "value": 'Isfara',
                "label":  'Исфара'},
        {
                "value": 'Ishkamshim',
                "label":  'Ишкашим'},
        {
                "value": 'Kabodien',
                "label":  'Кабодиён'},
        {
                "value": 'Kanibadam',
                "label":  'Канибадам'},
        {
                "value": 'Kulyab',
                "label":  'Куляб'},
        {
                "value": 'Kushonien',
                "label":  'Кушониён (Бохтар)'},
        {
                "value": 'Lahsh',
                "label":  'Лахш (Джиргиталь)'}, 
        {
                "value":'Levakand',
                "label":  'Леваканд (Сарбанд)'},
        {
                "value": 'Matcha',
                "label":  'Матча'},
        {
                "value": 'Muminabad',
                "label":  'Муминабад'},
        {
                "value": 'Murgab',
                "label":  'Мургаб'},
        {
                "value": 'Nosiri Husrav',
                "label":  'Носири Хусрав'},
        {
                "value": 'Nurabad',
                "label":  'Нурабад'},
        {
                "value": 'Nurek',
                "label":  'Нурек'},
        {
                "value": 'Pendjakent',
                "label":  'Пенджикент'},
        {
                "value": 'Pyandzh',
                "label":  'Пяндж'},
        {
                "value": 'Rasht',
                "label":  'Рашт'},
        {
                "value": 'Rogun',
                "label":  'Рогун'},
        {
                "value": 'Roshtkala',
                "label":  'Рошткала'},
        {
                "value": 'Rudaki',
                "label":  'Рудаки'},
        {
                "value": 'Rushan',
                "label":  'Рушан'},
        {
                "value": 'Sangvor',
                "label":  'Сангвор (Тавильдара)'},
        {
                "value": 'Spitamen',
                "label":  'Спитамен'},
        {
                "value": 'Tadzhikabad',
                "label":  'Таджикабад'},
        {
                "value": 'Temurmalik',
                "label":  'Темурмалик'},
        {
                "value": 'Tursunzade',
                "label":  'Турсунзаде'},
        {
                "value": 'Faizabad',
                "label":  'Файзабад'},
        {
                "value": 'Farhor',
                "label":  'Фархор'},
        {
                "value": 'Hamadani',
                "label":  'Хамадани'},
        {
                "value": 'Hovaling',
                "label":  'Ховалинг'},
        {
                "value": 'Horog',
                "label":  'Хорог'},
        {
                "value": 'Huroson',
                "label":  'Хуросон'},
        {
                "value": 'ShamsiddinShohin',
                "label":  'Шамсиддин Шохин (Шуроабад)'},
        {
                "value": 'Shahrinav',
                "label":  'Шахринав'},
        {
                "value": 'Shariston',
                "label":  'Шахристон'},
        {
                "value": 'Shahritus',
                "label":  'Шахритус'},
        {
                "value": 'Shugan',
                "label":  'Шугнан'},
        {
                "value": 'Yavan',
                "label":  'Яван'}

        ]
    }

class prepayment_data():
    value =   {
         "prpt_one":"1 месяц",
         "prpt_two":"2 месяца",
         "prpt_three":"3 месяца",
         "prpt_four":"4 месяца",
         "prpt_five":"5 месяцев",
         "prpt_six":"6 месяцев",
         "prpt_seven":"7 месяцев",
         "prpt_eight":"8 месяцев",
         "prpt_nine":"9 месяцев",
         "prpt_ten":"10 месяцев",
         "prpt_eleven":"11 месяцев",
         "prpt_year":"1 год"
               }

class info(object):
    value= {
            "object":"Тип обьекта",
            "area":"Площадь",
            'area_land':"Площать участка",
            "area_room":"Площадь комнат", 
            'area_house':'Площадь дома',
            "area_building":'Площадь здания',
            'ground_type':'Тип участка',
            "count_rooms":"Количетсво комнат", 
            "count_rooms_rent":"Количество комнат в аренду",
            'office_type':'Тип здания',
            "floor":"Этаж",
            "floorsHouse":"Этажей в доме",
            'floors_building':'Этажей',
            "building_type":"Тип здания",
            "building_renovation":"Тип ремонта",
            "city":"Город",
           }

class price_info(object):
    value= {
            "deal":"Тип сделки",
            "price":"Цена",
            "type_sell":"Тип продажи",
            "price_mounth":"Цена за месяц",
            "deposit":"Депозит",
            "prepayment":"Предоплата",
            "for_who":"Состав съемщиков",
           }
