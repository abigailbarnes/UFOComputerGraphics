import numpy as np
#import matplotlib.pyplot as plt

class BSpline:
    def __init__(self, t, c, d):
        """
        t = knots
        c = bspline coeff
        d = bspline degree
        """
        self.t = t
        self.c = c
        self.d = d
        assert self.is_valid()

    def is_valid(self) -> bool:
    #TODO: Q? -- complete this function.
        #slide 51 in lecture 11
        #d = m - n - 1
        #degree = knots - control_points - 1
        #knots are the locations that we are setting the values
        #typically want to use cubic polynomials
        
        
        #print(self.d, self.c, self.t)

        degree = self.d
        num_control_points = len(self.c)
        num_knots = len(self.t)

        #print(degree, num_control_points, num_knots)

        if degree < 1 or num_control_points < 1 or num_knots < num_control_points + degree + 1 or num_knots > num_control_points + degree + 1:
            return False
            #print("false")
        if not all(self.t[i] <= self.t[i+1] for i in range(num_knots-1)):
            #print("false")
            return False
        else:
            #print("true")
            return True


    def bases(self, x, k, i):
        #print('here')
        if k <= 1:
            if self.t[i] <= x < self.t[i+1]:
                return 1
            else:
                return 0
        else:
            ans = 0
            if(((self.t[i + k - 1] - self.t[i]) > 0) and ((self.t[i + k] - self.t[i + 1]) > 0)):
                #print('here')
                #print(k)
                #print(i + k - 1)
                ans += ((x - self.t[i]) / (self.t[i + k - 1] - self.t[i]) * self.bases(x, (k - 1), i)) + ((self.t[i + k] - x) / (self.t[i + k] - self.t[i + 1])) * self.bases(x, k - 1, i + 1)
                return ans
            '''if self.t[i+k] - self.t[i] > 0:
                ans += (x - self.t[i])/(self.t[i+k] - self.t[i]) * self.bases(x, k-1, i)
            if self.t[i+k+1] - self.t[i+1] > 0:
                ans += (self.t[i+k+1] - x)/(self.t[i+k+1] - self.t[i+1]) * self.bases(x, k-1, i+1)'''


    #helper function to search over the knots to see where the value lies between
    #find the index such that t[i] is less than or equal to the index value 

    def interp(self, x):
        bspline_sum = 0
        for i in range(len(self.c)):
            bspline_sum += self.c[i] * self.bases(x, self.d + 1, i)
        return bspline_sum
        
        
    

if __name__ == '__main__':
    
    #is_valid True test
    '''#16
    t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15] # set some knots. change this.
    #13
    control_colors = [0, 1, 3, 4, 3, 5, 7, 5, 4, 8, 9, 8, 7]
    d = 2 # set the degree.'''

    #7
    t = [0, 60, 65, 70, 75, 80, 100] # set some knots. change this.
    #4
    control_colors = [6.38438, 5, 6.38438, 8]
    d = 2 # set the degree.

    '''
    #is_valid false test; decreasing knots
    t = [0, 1, 3, 2, 4, 5] # set some knots
    control_colors = [[1, 0.2, 0.6], [0.4, 0.4, 1], [0.2, 0.8, 0.2]] # set some control colors
    d = 2 # degree
    '''

    '''
    #is_valid False test; incorrect knots = control points + degree + 1 evaluation
    t = [0, 1, 2, 3, 4, 5, 6] # set some knots. change this.
    control_colors = [[1, 0.2, 0.6], [0.4, 0.4, 1], [0.2, 0.8, 0.2]] # set some control colors. change this.
    d = 2 # set the degree. 
    '''

    '''
    t = [0, 1, 2, 3, 4, 5, 6, 7, 8] # set some knots. change this.
    control_colors = [[1, 0.2, 0.6], [0.4, 0.4, 1], [0.2, 0.8, 0.2]] # set some control colors. change this.
    d = 2
    '''

    spline = BSpline(t, control_colors, d)
    # now interpolate at some value
    #value = 2 #  change this.
    xs = np.linspace(t[0], t[-1], 100)
    #s = spline.interp(value)
    #spline.interp(value)
    ys = [spline.interp(x) for x in xs]
    knot_ys = [spline.interp(tval) for tval in t]
    #print(s)
    #print(knot_ys)
    #print(ys)
    print(len(ys))

    #print(len(t), len(control_colors), len(ys))
    
    
    #plt.plot(t, control_colors, 's', label='control points')
    '''plt.plot(xs, ys, label='line 2')
    plt.scatter(t, knot_ys)
    plt.legend()
    plt.show()'''