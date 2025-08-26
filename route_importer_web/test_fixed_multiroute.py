#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修复后的多路线功能
"""

import requests
import json

def test_fixed_multiroute():
    """测试修复后的多路线功能"""
    
    # 使用东京旅游笔记内容直接测试API
    tokyo_note = {
        "text": """
小红书

日本东京city walk旅游线路强烈推荐！个人向

-Day1[打卡R]新宿御苑，市中心很舒服的公园，里面的造景能感受到日本园林的特点[打卡R]东京都厅，免费的观景台，完全不输其他那些收费的观景台，强烈推荐[打卡R]新宿，一大片都很好逛，吃喝玩乐买买买，歌舞伎町也在这一片，转一圈出来继续买买买 

-Day2[打卡R]东京塔，个人感觉还是在别处远观更有感觉[打卡R]虎之门之丘、麻布台之丘、六本木之丘，都是很有个性的超级商业综合体，对于我这种建筑爱好者来说太有吸引力了，后面可以单独介绍一下这几个"丘"；上面都有观景台，可以选一个登上去看看[打卡R]国立新美术馆，黑川纪章设计的 

-Day3[打卡R]东京站，很有年代感的车站了，大穹顶很漂亮[打卡R]丸之内、新丸之内都很好逛，里面也会有很多艺术展，质量很高的那种；要去丸之内的屋顶拍照，很魔幻[打卡R]皇居，日本天皇住的地方，远不及国内的宫殿-个人向[doge]，如果没时间不用特意进去，哈哈哈哈 

-Day4[打卡R]浅草寺，经典打卡点，对于中国人来说可能会失望，古刹还是得看国内的[打卡R]东京国立博物馆，主馆主要介绍日本，东洋馆里面大部分是中国文物，最值得逛；逛国外的博物馆还是建议找个讲解，比如@东京国立博物馆讲解杨大眼 [doge] [打卡R]国立西洋美术馆，去的时候正好碰上莫奈特展，应该是到25年2月[打卡R]秋叶原，二次元朝圣地，喜欢二次元的同学可以单独逛逛这里 

-Day5[打卡R]代官山、表参道，这一片都是潮人聚集地[打卡R]涩谷，最繁忙的路口，忠犬八公像、涩谷sky观景台都在这 

-Day6[打卡R]银座，简直是购物天堂，在这里几乎可以买到你想买的所有东西，这次住这附近一有空就能逛逛[大笑R] 

#东京旅行 #日本旅行 #东京city_walk #银座 #新宿 #东京塔 #东京国立博物馆 #新年旅行第一站
"""
    }
    
    print("🧪 测试修复后的多路线功能")
    print("=" * 50)
    
    try:
        # 直接调用AI解析器，绕过URL解析
        response = requests.post(
            'http://localhost:8081/api/parse-note',
            json=tokyo_note,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print("✅ API调用成功！")
                data = result['data']
                print(f"标题: {data.get('title', 'N/A')}")
                
                # 检查多路线结构
                if 'routes' in data and data['routes']:
                    print(f"🗺️ 识别到 {len(data['routes'])} 条路线:")
                    total_places = 0
                    for i, route in enumerate(data['routes'], 1):
                        places = route.get('places', [])
                        total_places += len(places)
                        print(f"  路线{i}: {route.get('route_name', 'N/A')} ({len(places)}个地点)")
                    
                    print(f"\n📍 总计: {total_places} 个地点")
                    
                elif 'places' in data:
                    print(f"📍 单路线地点数量: {len(data['places'])}")
                
                print(f"\n🏷️  标签: {', '.join(data.get('tags', [])[:5])}")
                
            else:
                print(f"❌ API调用失败: {result.get('error', 'N/A')}")
                
        else:
            print(f"❌ HTTP错误 {response.status_code}")
            print(f"响应: {response.text}")
            
    except Exception as e:
        print(f"❌ 测试异常: {str(e)}")

if __name__ == '__main__':
    test_fixed_multiroute()
