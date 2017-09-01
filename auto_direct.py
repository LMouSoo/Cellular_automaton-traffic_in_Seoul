import numpy
import time
import copy


cross_on_term = 60
cross_off_term = 30
traffic_rate = 0.1
road_r = 32
road_l = 64

cell_empty = 0
cell_road = 1
cell_cross_NS = 2
cell_cross_EW = 5
cell_car = 3

direction_N = 0
direction_E = 1
direction_W = 2
direction_S = 3

# init road
numpy.random.seed(0)

tic_field = numpy.zeros((road_r,road_l),dtype=int)

tic_field[8,1:road_l-1] = cell_road
tic_field[10,1:road_l-1] = cell_road
tic_field[24,1:road_l-1] = cell_road
tic_field[26,1:road_l-1] = cell_road
tic_field[1:road_r-1,16] = cell_road
tic_field[1:road_r-1,18] = cell_road
tic_field[1:road_r-1,48] = cell_road
tic_field[1:road_r-1,50] = cell_road

tic_field[8,16] = (cross_on_term<<4)+cell_cross_EW
tic_field[8,18] = (cross_on_term<<4)+cell_cross_EW
tic_field[10,16] = (cross_on_term<<4)+cell_cross_EW
tic_field[10,18] = (cross_on_term<<4)+cell_cross_EW
tic_field[8,48] = (cross_on_term<<4)+cell_cross_EW
tic_field[8,50] = (cross_on_term<<4)+cell_cross_EW
tic_field[10,48] = (cross_on_term<<4)+cell_cross_EW
tic_field[10,50] = (cross_on_term<<4)+cell_cross_EW
tic_field[24,16] = (cross_on_term<<4)+cell_cross_EW
tic_field[24,18] = (cross_on_term<<4)+cell_cross_EW
tic_field[26,16] = (cross_on_term<<4)+cell_cross_EW
tic_field[26,18] = (cross_on_term<<4)+cell_cross_EW
tic_field[24,48] = (cross_on_term<<4)+cell_cross_EW
tic_field[24,50] = (cross_on_term<<4)+cell_cross_EW
tic_field[26,48] = (cross_on_term<<4)+cell_cross_EW
tic_field[26,50] = (cross_on_term<<4)+cell_cross_EW

toc_field = copy.deepcopy(tic_field)


#loop

# moving car
for loop in range(100000000) :
    for i in range(road_r) :
        for j in range(road_l) :
            if tic_field[i,j]&15 == cell_car :
                check_direction = tic_field[i,j] >> 4
                if check_direction == direction_N :
                    if toc_field[i-1,j] == cell_road :
                        toc_field[i-1,j] = (direction_N<<4)+cell_car
                        toc_field[i,j] = cell_road
                    if tic_field[i-1,j]&15 == cell_cross_NS :
                        if toc_field[i-2,j] == cell_road :
                            toc_field[i-2,j] = (direction_N<<4)+cell_car
                            toc_field[i,j] = cell_road
                    if toc_field[i-1,j] == cell_empty :
                        toc_field[i,j] = cell_road

                if check_direction == direction_E :
                    if toc_field[i,j+1] == cell_road :
                        toc_field[i,j+1] = (direction_E<<4)+cell_car
                        toc_field[i,j] = cell_road
                        ##print(tic_field==toc_field)
                    if tic_field[i,j+1]&15 == cell_cross_EW :
                        if toc_field[i,j+2] == cell_road :
                            toc_field[i,j+2] = (direction_E<<4)+cell_car
                            toc_field[i,j] = cell_road
                    if toc_field[i,j+1] == cell_empty :
                        toc_field[i,j] = cell_road

                if check_direction == direction_W :
                    if toc_field[i,j-1] == cell_road :
                        toc_field[i,j-1] = (direction_W<<4)+cell_car
                        toc_field[i,j] = cell_road
                    if tic_field[i,j-1]&15 == cell_cross_EW :
                        if toc_field[i,j-2] == cell_road :
                            toc_field[i,j-2] = (direction_W<<4)+cell_car
                            toc_field[i,j] = cell_road
                    if toc_field[i,j-1] == cell_empty :
                        toc_field[i,j] = cell_road
        
                if check_direction == direction_S :
                    if toc_field[i+1,j] == cell_road :
                        toc_field[i+1,j] = (direction_S<<4)+cell_car
                        toc_field[i,j] = cell_road
                    if tic_field[i+1,j]&15 == cell_cross_NS :
                        if toc_field[i+2,j] == cell_road :
                            toc_field[i+2,j] = (direction_S<<4)+cell_car
                            toc_field[i,j] = cell_road
                    if toc_field[i+1,j] == cell_empty :
                        toc_field[i,j] = cell_road

            if tic_field[i,j]&15 == cell_cross_EW :
                check_time = tic_field[i,j] >> 4
                if check_time == 0 :
                    toc_field[i,j] = (cross_off_term << 4)+cell_cross_NS
                else :
                    check_time -= 1
                    toc_field[i,j] = (check_time << 4)+cell_cross_EW

            if tic_field[i,j]&15 == cell_cross_NS :
                check_time = tic_field[i,j] >> 4
                if check_time == 0 :
                    toc_field[i,j] = (cross_on_term << 4)+cell_cross_EW
                else :
                    check_time -= 1
                    toc_field[i,j] = (check_time << 4)+cell_cross_NS


    # loading car
    if toc_field[10,1] == cell_road :
        if numpy.random.rand() < traffic_rate :
            toc_field[10,1] = (direction_E<<4)+cell_car

    if toc_field[26,1] == cell_road :
        if numpy.random.rand() < traffic_rate :
            toc_field[26,1] = (direction_E<<4)+cell_car

    if toc_field[8,road_l-2] == cell_road :
        if numpy.random.rand() < traffic_rate :
            toc_field[8,road_l-2] = (direction_W<<4)+cell_car

    if toc_field[24,road_l-2] == cell_road :
        if numpy.random.rand() < traffic_rate :
            toc_field[24,road_l-2] = (direction_W<<4)+cell_car

    if toc_field[1,16] == cell_road :
        if numpy.random.rand() < traffic_rate :
            toc_field[1,16] = (direction_S<<4)+cell_car

    if toc_field[1,48] == cell_road :
        if numpy.random.rand() < traffic_rate :
            toc_field[1,48] = (direction_S<<4)+cell_car

    if toc_field[road_r-2,18] == cell_road :
        if numpy.random.rand() < traffic_rate :
            toc_field[road_r-2,18] = (direction_N<<4)+cell_car

    if toc_field[road_r-2,50] == cell_road :
        if numpy.random.rand() < traffic_rate :
            toc_field[road_r-2,50] = (direction_N<<4)+cell_car

    # print road
    for i in range(road_r):
        for j in range(road_l):
            print(toc_field[i,j]&15,end='')
        print('')

    tic_field = copy.deepcopy(toc_field)

    time.sleep(0.1)
