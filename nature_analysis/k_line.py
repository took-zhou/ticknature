from data_generator.reader import fileReader as FR


# paramInput = {
#     "instruments": [
#         {
#             "exchangeId": "DCE",
#             "instrumentId": "c2103"
#         },
#         {
#             "exchangeId":  "DCE",
#             "instrumentId":"c2105"
#         },
#         # {
#         #     "exchangeId":  "SHFE",
#         #     "instrumentId":"AL1701"
#         # }
#     ],
#     "exchanges": ["DCE", "SHFE"],
#     "duration": {
#         "begin": "2020-11-12-09:00:00.0",
#         "end": "2020-11-12-15:00:00.0"
#     },
#     "targetFields": ["LastPrice"],
#     "nightMarket": True,  # 暂时不支持夜市数据读取，此处暂时只能填false,填true无效
#     "dayMarket": True,
#     "interval": 1,  # s
#     "simSleepInterval": 0.01,  # s 0.1s 输出真实1秒的数据，来控制仿真速度
#     "dataRootPath": "/share/baidunetdisk/reconstruct/tick"
# }

# paramSelf = {"type":"equidistant"}

# gen = FR.DataReader(paramInput)
# data = gen.dataGenForAnalysis(paramSelf)
# print(type(data))
# for v in data:
#     print(v)