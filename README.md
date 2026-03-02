

| 格式  | 文件名                               | 作用                             | 备注                                             |
| ----- | ------------------------------------ | -------------------------------- | ------------------------------------------------ |
| json  | injury_dict                          | 伤病页面的url                    |                                                  |
|       | player_dict                          | 球员页面的url                    |                                                  |
|       | feature_data_dict                    | 球员特征数据                     |                                                  |
|       | feature_data_dict_p                  | 同上（不含联赛）                 | 少两个球员                                       |
|       | injury_data_dict                     | 球员伤病数据                     |                                                  |
|       | injury_data_dict_p                   | 同上（不含联赛）                 | 少两个球员                                       |
|       | obj_dict                             | 球员对象                         | 完整数据                                         |
|       | obj_list                             | 同上（不含联赛）                 | 完整数据                                         |
|       | sorted_injury_data_dict              | 纠错过程中产生的，没用           | 可删除                                           |
|       | keyword_to_category                  | 数据分析过程中产生的，讲伤病分类 |                                                  |
|       | keyword_to_category_cu               | 同上                             | 中文                                             |
| ipynb | (unsuccessful)_PART1_datafetch       | 最初的爬取实验                   |                                                  |
|       | PART1_datafetch                      | 获取数据源                       | 成果：设计爬取模式，得到injury_dict与player_dict |
|       | PART2_abstraction_and_data_structure | 结构化数据                       | 成果：设计数据结构，得到obj_list                 |
|       | PART2_(extra)_loading_objects        | 测试加载球员对象数据             |                                                  |
|       | PART3_analyzing_and_visualization    | 数据分析与可视化                 |                                                  |
|       | PART4_prediction_model               | 预测模型                         | 未完成                                           |
| html  | rodri                                | 爬取过程中的一个测试             | 可删除                                           |
| py    | player                               | 球员对象                         | 自定义模块                                       |
|       | scraper_util.py                      | 爬虫                             | 自定义模块                                       |
| txt   | keyword_to_category                  | gpt生成，经修改写成了json        |                                                  |
| exe   | chromedriver                         | selenium                         | 尝试，实际并未用到                               |