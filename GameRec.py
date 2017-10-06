import csv
from math import sqrt

class AutoVivification(dict):
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

def main():
    dataset = AutoVivification()
    filename = 'usersnratings.csv'
    with open(filename, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for row in reader:
            dataset[row[0]][row[1]] = row[2]
            
    def pearson(p1,p2):
        both={}
        for item in dataset[p1]:
            if item in dataset[p2]:
                both[item] = 1
        num_rating = len(both)
        if num_rating == 0 :
            return 0
        p1_ssq = sum([pow(int(dataset[p1][item]),2) for item in both])
        p1_sp = sum([int(dataset[p1][item]) for item in both])
        p1_s =  p1_ssq-(pow(p1_sp,2)/num_rating)
        
        p2_ssq = sum([pow(int(dataset[p2][item]),2) for item in both])
        p2_sp = sum([int(dataset[p2][item]) for item in both])
        p2_s =  p2_ssq-(pow(p2_sp,2)/num_rating)
        
        denom = sqrt(p1_s * p2_s)
        
        prod_both = sum([int(dataset[p1][item]) * int(dataset[p2][item]) for item in both])
        
        num = prod_both - ((p1_sp * p2_sp)/num_rating)
        
        if denom == 0 :
            return 0
        else :
            r = num/denom
            return r
        
    def recommend(per):
        total = {}
        sim_sum = {}
        
        for other in dataset :
            if other == per:
                continue
            sim = pearson(per,other)
            
            if sim <= 0 :
                continue
            for item in dataset[other]:
                if item not in dataset[per] or dataset[per][item] == 0 :
                    total.setdefault(item,0)
                    total[item] += int(dataset[other][item])*sim
                    sim_sum.setdefault(item,0)
                    sim_sum[item] += sim
                           
        rank = [(tot/sim_sum[item],item) for item,tot in total.items()]
        rank.sort()
        rank.reverse()
          
        recom_list = [recommend_item for recommend_item,recommend_item in rank]
        return recom_list[0:5]
   
    print ("GameRec\n")
    n=input("Enter User ID ")
    n1 = int(n)
    if n1 > len(dataset):
        print("\nUser ID does not exist")
    else:
        print("\nRecommendations for User %d\n" % n1)
        print(recommend('User %d' % n1))
    
if __name__ == '__main__':
    main()
