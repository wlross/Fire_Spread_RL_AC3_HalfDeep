import pandas as pd
import random
import time

def get_neighbors(index,data):
    thisLeft = data.loc[index, 'left']
    thisTop = data.loc[index, 'top']
    thisRight = data.loc[index, 'right']
    thisBottom = data.loc[index, 'bottom']

    upCell = data[data['top'] == thisBottom]
    upCell = upCell[upCell['left'] == thisLeft]
    if upCell.empty:
        upCell = None
    else:
        upCell = upCell['id'].iloc[0]

    downCell = data[data['bottom'] == thisTop]
    downCell = downCell[downCell['right'] == thisRight]
    if downCell.empty:
        downCell = None
    else:
        downCell = downCell['id'].iloc[0]

    leftCell = data[data['left'] == thisRight]
    leftCell = leftCell[leftCell['top'] == thisTop]
    if leftCell.empty:
        leftCell = None
    else:
        leftCell = leftCell['id'].iloc[0]

    rightCell = data[data['right'] == thisLeft]
    rightCell = rightCell[rightCell['bottom'] == thisBottom]
    if rightCell.empty:
        rightCell = None
    else:
        rightCell = rightCell['id'].iloc[0]

    return(upCell, downCell, leftCell, rightCell)


qTable = pd.read_csv("Qtable.csv")
start = 1
decay = .95

#TODO Make multiple iterations
for i in range (0,20):
    data = pd.read_csv("FinalGrid_All.csv")
    onFire = data[data['Nov8Fire'] == 1]
    for j in range(0,10):
        tik = time.time()
        if j>0:
            onFire = data[data['Nov9Pred'] == 1]
        myLambda = decay ** i
        for index, row in onFire.iterrows():
            up, down, left, right = get_neighbors(index, data)
            neighbors = [up, down, left, right]
            for neighbor in neighbors:
                if neighbor == None:
                    continue
                if data.loc[neighbor, 'Nov8Fire'] == 1:
                    continue
                else:
                    #print("determine action")
                    #print(index)
                    #print(neighbor)
                    elevation = data.loc[neighbor, 'elevation']
                    speed = data.loc[neighbor, 'speed']
                    direction = data.loc[neighbor, 'dir']
                    burnable = data.loc[neighbor, 'burnable']
                    state = str(elevation) + '-' + str(speed) + '-' + str(direction) + '-' + str(burnable)
                    #print(state)
                    burnVal = qTable.loc[qTable['State'] == state]['1'].values[0]
                    noVal = qTable.loc[qTable['State'] == state]['0'].values[0]
                    myDex = qTable.loc[qTable['State'] == state]['0'].index[0]
                    if burnVal>noVal:
                        action = '1'
                    else:
                        action = '0'
                    if random.uniform(0,1) < myLambda:
                        #print("random")
                        if random.uniform(0,1) < .5:
                            action = '1'
                        else:
                            action = '0'
                    if action == '1':
                        data.loc[neighbor,'Nov9Pred'] = 1
                    else:
                        data.loc[neighbor, 'Nov9Pred'] = 0
                    if data.loc[neighbor, 'Nov9Pred'] - data.loc[neighbor, 'Nov9Fire'] != 0:
                        if qTable.loc[myDex, action] > 0:
                            qTable.loc[myDex, action] -= 10
                        else:
                            qTable.loc[myDex, action] -= 1
                    else:
                        qTable.loc[myDex, action] += 1
        tok = time.time()
        print(tok-tik)
        print(i)
        print(j)
    data.to_csv('newGridAll.csv')
    qTable.to_csv('newPolicy.csv')





