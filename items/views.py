# -*- coding: utf-8 -*-
import json
import requests
import copy

from django.shortcuts import render

option_city = {'3008': 'Martlock', '0007': 'Thetford', '2004': 'Bridgewatch', '3005': 'Caerleon',
               '1002': 'Lymhurst', '4002': 'Fort Sterling'}
option_items = {'mellee_sword': 'Мечи', 'range': 'Оружие дальнего боя', 'mellee_mace': 'Булавы',
                'mellee_staff': 'Шесты', 'mellee_hammer': 'Молоты', 'mellee_daggers': 'Кинжалы', 'mellee_axe': 'Топоры',
                'staff': 'Посохи/Магия', 'plate_shoes': 'Латные ботинки', 'plate_head': 'Латные шлемы',
                'plate_armor': 'Латные доспехи', 'leather_shoes': 'Кожанные ботинки',
                'leather_head': 'Кожанные капюшоны', 'leather_armor': 'Кожанные доспехи',
                'cloth_shoes': 'Тканевые ботинки', 'cloth_armor': 'Тканевые доспехи', 'cloth_head': 'Тканевые колпаки',
                'capes': 'Плащи', 'bags': 'Сумки'}
option_tier = ['T4', 'T5', 'T6', 'T7', 'T8']
quality_level = {1: 'Обычное', 2: 'Хорошее', 3: 'Потрясающее', 4: 'Превосходное', 5: 'Шедевр'}

API = 'https://www.albion-online-data.com/api/v2/stats/prices/'

with open('items/static/items/items.json', 'r') as f:
    full_name = json.load(f)
with open('items/static/items/russia.json', 'r', encoding='utf-8') as f:
    russia_name = json.load(f)


def index(request):
    return render(request, 'index.html', context={'cities': option_city, 'items': option_items, 'tiers': option_tier, })


def search(request):
    global price_black_order
    query_items = []
    items_view = {}
    list_item_view = []
    city = request.GET.get('city')
    item = request.GET.get('item')
    tiers = request.GET.getlist('tier')
    charts = request.GET.getlist('chart')
    profit = request.GET.get('profit').strip()
    items = full_name[item]
    item_name = ''
    price_market = 0
    img_url = ''
    error = False
    for i in range(0, len(items)):
        for tir in range(0, len(tiers)):
            for chart in range(0, len(charts)):
                if charts[chart] == '0':
                    full_item = f'{tiers[tir]}_{items[i]}'
                else:
                    full_item = f'{tiers[tir]}_{items[i]}{charts[chart]}'
                query_items.append(full_item)
    url_json = API + ','.join(query_items) + '?locations=' + '3003,' + option_city[city]
    response_api = requests.get(url_json).json()
    for i in range(0, len(response_api)):
        qs_dict = response_api[i]
        if qs_dict['buy_price_min_date'] == "0001-01-01T00:00:00" \
                or qs_dict['sell_price_min_date'] == "0001-01-01T00:00:00" \
                or qs_dict['sell_price_max_date'] == "0001-01-01T00:00:00" \
                or qs_dict['buy_price_max_date'] == "0001-01-01T00:00:00":
            continue
        else:
            if qs_dict['city'] != 'Black Market':
                price_market = qs_dict['sell_price_min']
                items_view['price_market'] = '{:,}'.format(price_market).replace(',', '.')
            else:
                for k, v in russia_name.items():
                    if k == qs_dict['item_id'][3:]:
                        item_name = v[0]
                quality = qs_dict['quality']
                items_view['quality'] = quality_level[quality]
                items_view['item_name'] = item_name
                item_name_img = qs_dict['item_id']
                price_black_order = qs_dict['sell_price_min']
                items_view['price_black_order'] = '{:,}'.format(price_black_order).replace(',', '.')
                total_price_order = price_black_order - price_market
                items_view['total_price_order'] = '{:,}'.format(total_price_order).replace(',', '.')
                price_black_fast = qs_dict['buy_price_max']
                items_view['price_black_fast'] = '{:,}'.format(price_black_fast).replace(',', '.')
                total_price_fast = price_black_fast - price_market
                items_view['total_price_fast'] = '{:,}'.format(total_price_fast).replace(',', '.')
                time_upd = qs_dict['buy_price_max_date']
                items_view['time_add'] = time_upd
                img_url = 'https://albionmarketdiff.ru/img/' + item_name_img + '.png'
                list_item_view.append(copy.deepcopy(items_view))
                if not profit:
                    profit = 1
                if total_price_order > int(profit):
                    list_item_view.append(copy.deepcopy(items_view))
                else:
                    pass
    return render(request, 'index.html', context={'cities': option_city, 'items': option_items, 'tiers': option_tier,
                                                  'town': option_city[city], 'item_name': item_name, 'error': error,
                                                  'list_item_view': list_item_view, 'img_url': img_url})