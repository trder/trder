from guitree import *
from GuiPage.TradingSystemInfoPage import *

guidata = guitree("trder量化平台",
                  guitree("交易系统",
                          guitree("创建交易系统",
                                  guitree("API参考文档",
                                          None,
                                          None
                                          ),
                                  guitree("开始创建",
                                          None,
                                          None
                                          )
                                  ),
                          guitree("浏览交易系统",
                                  guitree("交易系统商店",
                                          guitree("官方交易系统",
                                                guitree("官方机械交易系统",
                                                        guitree("官方趋势交易系统",
                                                                guitree("唐奇安趋势突破交易系统",
                                                                        None,
                                                                        None,
                                                                        TradingSystemInfoPage("唐奇安趋势突破交易系统",
                                                                        '''唐奇安趋势系统，它是当年的海龟系统的一个简化版本。
                                                                        趋势方向：如果25日均线在350日均线之上，只能做多；如果25日均线在350日均线之下，只能做空。
                                                                        趋势过滤：它采用20日最高点突破入市策略。20日最高点突破开多；跌破20日最低点开空。'''
                                                                        )
                                                                        ),
                                                                guitree("MACD趋势突破交易系统",
                                                                        None,
                                                                        None,
                                                                        TradingSystemInfoPage("MACD趋势突破交易系统",
                                                                        ""
                                                                        )
                                                                        )
                                                                ),
                                                        guitree("官方反趋势交易系统",
                                                                None,
                                                                None
                                                                )
                                                        ),
                                                guitree("官方AI交易系统",
                                                        None,
                                                        None
                                                        )
                                                  ),
                                          guitree("第三方交易系统",
                                                  None,
                                                  None
                                                  )
                                          ),
                                  guitree("本地交易系统",
                                          None,
                                          None
                                          )
                                  )
                          ),
                  guitree("开始交易",
                          guitree("模拟交易",
                                  guitree("选项1",
                                          None,
                                          None
                                          ),
                                  guitree("选项2",
                                          None,
                                          None
                                          )
                                  ),
                          guitree("实盘交易",
                                  guitree("选项1",
                                          None,
                                          None
                                          ),
                                  guitree("选项2",
                                          None,
                                          None
                                          )
                                  )
                          ),
                  )