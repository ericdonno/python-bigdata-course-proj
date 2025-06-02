from collections import namedtuple
from datetime import datetime # 使用namedtuple来实现简单数据容器

Healthy = namedtuple('Healthy',['days'])
Injured = namedtuple('Injured',['days', 'injury','games_missed'])    # int str int


def player_to_dict(player):
    """
        seriallize a player object
    """
    player_dict = player.__dict__.copy()
    
    # 转换 Healthy 和 Injured 为可序列化的字典
    def convert_to_dict(obj):
        if isinstance(obj, (Healthy, Injured)):
            return obj._asdict()  
        return obj 
    player_dict['injury_history'] = [convert_to_dict(item) for item in player_dict['injury_history']]
    
    # apparence 是一个元组，转换为列表
    player_dict['apparence'] = list(player_dict['apparence'])
    return player_dict


def obj_list_from_json(obj_list):
    """
        it's destructive
    """
    def inj_type_from_dict(d):
        if 'days' in d and 'injury' not in d:  # 判断 Healthy
            return Healthy(d['days'])
        elif 'days' in d and 'injury' in d:  # 判断 Injured 
            return Injured(d['days'], d['injury'], d['games_missed'])
        else:
            raise Exception("Error convering object from dict")
            
    for p in obj_list:
        p['injury_history'] = [inj_type_from_dict(data) for data in p['injury_history']]
        p['apparence'] = tuple(p['apparence'])
        
    return obj_list


def obj_dict_from_json(obj_dict):
    """
        it's destructive
    """
    def inj_type_from_dict(d):
        if 'days' in d and 'injury' not in d:  # 判断 Healthy
            return Healthy(d['days'])
        elif 'days' in d and 'injury' in d:  # 判断 Injured 
            return Injured(d['days'], d['injury'], d['games_missed'])
        else:
            raise Exception("Error convering object from dict")
    
    for ldict in obj_dict.values():
        for p in ldict.values():
            p['injury_history'] = [inj_type_from_dict(data) for data in p['injury_history']]
            p['apparence'] = tuple(p['apparence'])
    return obj_dict


class Player:
    still_injured = {"2025/6/1": []}
    
    def __init__(self, name, position, height, nationality, apparence=(0,0)):  
        if not all(isinstance(arg, str) for arg in (name, position, height, nationality)):
            raise TypeError("All attributes must be strings.")
        self.name = name
        self.position = position
        self.height = height
        self.nationality = nationality
        self.injury_history = []
        self.apparence = apparence
    
    def add_healthy(self, days):
        history = self.injury_history
        if history and isinstance(history[-1], Healthy):
            raise TypeError("Last history is healthy")
        history.append(Healthy(days))
#         print('added', Healthy(days))
        
    def add_injured(self, days, injury, games_missed):
        history = self.injury_history
        if history and isinstance(history[-1], Injured):
            raise TypeError("Last history is injured")
        history.append(Injured(days, injury, games_missed))
#         print('added', Injured(days, injury, games_missed))
        
    def get_all_injured(self):
        return self.injury_history[1::2]  # 切片有复制操作，时间复杂度为O(n)

    def average_apparence_min(self):
        if self.apparence == (0,0):
            return 0
        return self.apparence[1]/self.apparence[0]

    def generate_injury_history(self, injury_data):
        injury_data = injury_data.copy()  
        self.add_healthy(-1) 
        
        if injury_data:
            d = injury_data.pop()
            self.add_injured(d['days'], d['injury'], d['games_missed'])
            if d['util'] == '':
                print(f"\n球员: {self.name} 无限期伤病")
                Player.still_injured["2025/6/1"].append(self.name)
            else:
                until = d['util']
                last_injury_end = datetime.strptime(until, '%b %d, %Y')

                while injury_data:
                    d = injury_data.pop()
                    from_date = datetime.strptime(d['from'], '%b %d, %Y')
                    if d['util'] == '':
                        if injury_data:   # 如果injury_data不空，说明这个d不是最新的伤病数据。非最新的伤病数据有这个异常，是不正常的。
                            raise Exception(f"\n球员: {self.name} 数据异常")
                        print(f"\n球员: {self.name} 无限期伤病")
                        Player.still_injured["2025/6/1"].append(self.name)
                    else:
                        until = d['util']
                    until_date = datetime.strptime(until, '%b %d, %Y')

                    vec = (from_date - last_injury_end).days
                    if vec >= 0:
                        healthy_days = vec
                        self.add_healthy(healthy_days)

                        self.add_injured(d['days'], d['injury'], d['games_missed'])
                        last_injury_end = until_date  # 新数据的untill
                    else:
                        self.add_healthy(0)
                        self.add_injured(d['days'], d['injury'], d['games_missed'])
                        # 不修改 last_injury_end
                        
                        
                        
                    
    def get_inj_series(self):
        return [data['days'] for data in self.injury_history]
        
