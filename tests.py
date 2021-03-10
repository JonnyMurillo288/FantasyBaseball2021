import unittest
from stats_analysis import Fantasy

class ReturnDataFrame(unittest.TestCase):

    # def testget_stats_batter(self):
    #     df = Fantasy(name='Christian Yelich',id='592885',manual=True)
    #     position = df.cat_stats(df.name,df.id,check=True)
    #     df.year_to_year_statcast(df.name,df.id,position=position)
    #     df.cat_stats(df.name,df.id,position=position)
    #     shape = df.combine_stats(name=df.name,position=position)
    #     print(shape.shape)
    #     self.assertGreaterEqual(shape.shape[1], 300)
        
        

    def testget_stats_pitcher(self):
        df = Fantasy(name='Sixto Sanchez',id= '664350',manual=True)
        position = df.cat_stats(df.name,df.id,check=True)
        x = df.year_to_year_statcast(df.name,df.id,position=position)
        df.cat_stats(df.name,df.id,position=position)
        print(type(x))
        print(x)
        if x == 0 or x == '0':
            self.assertTrue(x.isnumeric())
            return 
        else:
            shape = df.combine_stats(name=df.name,position=position)
            self.assertGreaterEqual(shape.shape[1], 12)
        
        
